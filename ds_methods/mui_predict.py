import datetime as dt
import gc
import json
import logging
import os

import pandas as pd
import torch
from async_lru import alru_cache
from torch.utils.data import DataLoader
from tqdm.auto import trange

from app import UPLOAD_DIRECTORY, mui_df_path, mui_model
from utils.dataset import MUI_JDNDataset

logger = logging.getLogger("jdi-qasp-ml")


@alru_cache(maxsize=32)
async def mui_predict_elements(body):
    body_str = body.decode("utf-8")
    body_json = json.loads(body_str)
    elements_json = body_json.get("elements", [])

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
    df = pd.DataFrame(json.loads(elements_json))
    # fix bad data which can come in 'onmouseover', 'onmouseenter'
    df.onmouseover = df.onmouseover.apply(
        lambda x: "true" if x is not None else None
    )
    df.onmouseenter = df.onmouseenter.apply(
        lambda x: "true" if x is not None else None
    )
    df.to_pickle(f"{mui_df_path}/{filename}")
    logger.info("Creating JDNDataset")
    dataset = MUI_JDNDataset(
        datasets_list=[filename.split(".")[0]], rebalance_and_shuffle=False
    )
    dataloader = DataLoader(dataset, shuffle=False, batch_size=1)
    device = "cpu"
    logger.info(f"Load model with hardcoded device: {device}")
    model = torch.load(f"{mui_model}/model.pth", map_location="cpu").to(
        device=device
    )
    model.eval()
    logger.info("Predicting...")
    results = []
    with trange(len(dataloader)) as bar:
        with torch.no_grad():
            for x, y in dataloader:

                x.to(device)
                y.to(device)
                y_prob = (
                    softmax(model(x.to(device)).to("cpu")).detach().numpy()
                )

                y_pred = y_prob[0].argmax()

                if y != torch.tensor([0]):
                    logger.info(f"y is\n {y} ")
                    logger.info(f"y_pred is\n {y_pred} ")

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
    # # update the dataset with predictions
    dataset.df["predicted_label"] = results_df.y_pred_label.values
    dataset.df["predicted_probability"] = results_df.y_probability.values
    columns_to_publish = [
        "element_id",
        "predicted_label",
    ]
    results_df = dataset.df[(dataset.df["predicted_label"] != "n/a")].copy()

    # sort in ascending order by coordinates
    results_df = results_df.sort_values(by=["y", "x"], ascending=[True, True])

    if results_df.shape[0] == 0:
        gc.collect()
        return []
    else:
        del model
        gc.collect()
        return results_df[columns_to_publish].to_dict(orient="records")
