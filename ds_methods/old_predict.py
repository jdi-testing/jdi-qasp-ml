import datetime as dt
import gc
import json
import logging
import os
import pickle

import pandas as pd
import torch
from torch.utils.data import DataLoader
from tqdm.auto import trange

from app import UPLOAD_DIRECTORY, old_df_path, old_model
from utils_old import JDNDataset as Old_JDNDataset

logger = logging.getLogger("jdi-qasp-ml")


async def predict_elements(body):
    # create softmax layser function to get probabilities from logits
    softmax = torch.nn.Softmax(dim=1)
    # generate temporary filename
    filename = dt.datetime.now().strftime("%Y%m%d%H%M%S%f.json")
    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        logger.info(f"saving {filename}")
        fp.write(body)
        fp.flush()
    filename = filename.replace(".json", ".pkl")
    logger.info(f"saving {filename}")
    df = pd.DataFrame(json.loads(body))
    # fix bad data which can come in 'onmouseover', 'onmouseenter'
    df.onmouseover = df.onmouseover.apply(lambda x: "true" if x is not None else None)
    df.onmouseenter = df.onmouseenter.apply(lambda x: "true" if x is not None else None)
    with open(f"{old_df_path}/{filename}.pkl", "wb") as f:
        pickle.dump(df, f)
        f.flush()
    df.to_pickle(f"{old_df_path}/{filename}")
    logger.info("Creating JDNDataset")
    dataset = Old_JDNDataset(
        datasets_list=[filename.split(".")[0]], rebalance_and_shuffle=False
    )
    dataloader = DataLoader(dataset, shuffle=False, batch_size=1)
    device = "cpu"
    logger.info(f"Load model with hardcoded device: {device}")
    model = torch.load(f"{old_model}/model.pth", map_location="cpu").to(device=device)
    model.eval()
    logger.info("Predicting...")
    results = []
    with trange(len(dataloader)) as bar:
        with torch.no_grad():
            for x, y in dataloader:
                x.to(device)
                y.to(device)
                y_prob = softmax(model(x.to(device)).to("cpu")).detach().numpy()

                y_pred = y_prob[0].argmax()
                y = y.item()
                y_prob = y_prob[0, y_pred].item()

                results.append(
                    {
                        "y_true": y,
                        "y_pred": y_pred,
                        "y_probability": y_prob,
                        "y_true_label": dataset.classes_reverse_dict[y],
                        "y_pred_label": dataset.classes_reverse_dict[y_pred],
                    }
                )
                bar.update(1)
    results_df = pd.DataFrame(results)
    # update the dataset with predictions
    dataset.df["predicted_label"] = results_df.y_pred_label.values
    dataset.df["predicted_probability"] = results_df.y_probability.values
    columns_to_publish = [
        "element_id",
        "x",
        "y",
        "width",
        "height",
        "predicted_label",
        "predicted_probability",
    ]
    results_df = dataset.df[
        (dataset.df["predicted_label"] != "n/a")  # & (dataset.df['is_hidden'] == 0)
    ][columns_to_publish].copy()
    # sort in descending order: big controls first
    results_df["sort_key"] = results_df.height * results_df.width
    results_df = results_df.sort_values(by="sort_key", ascending=False)
    if results_df.shape[0] == 0:
        gc.collect()
        return []
    else:
        del model
        gc.collect()
        return results_df.to_json(orient="records")
