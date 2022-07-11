import datetime as dt
import gc
import json
import logging
import os
import pickle

import pandas as pd

from app import UPLOAD_DIRECTORY, html5_classes_path, html5_df_path, html5_model
from utils.dataset import HTML5_JDNDataset

logger = logging.getLogger("jdi-qasp-ml")


async def html5_predict_elements(body):
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

    df.to_pickle(f"{html5_df_path}/{filename}")

    logger.info("Creating JDNDataset")
    dataset = HTML5_JDNDataset(
        datasets_list=[filename.split(".")[0]],
        dataset_type="html5",
        rebalance_and_shuffle=False,
    )
    # load model
    logger.info("Loading the model")
    pkl_filename = "DT_model.pkl"
    with open(f"{html5_model}/{pkl_filename}", "rb") as file:
        model = pickle.load(file)

    # classes dictionaries
    with open(html5_classes_path, "r") as f:
        lines = f.readlines()
        encoder_dict = {line.strip(): i for i, line in enumerate(lines)}
        decoder_dict = {v: k for k, v in encoder_dict.items()}

    logger.info("Predicting...")
    dataset.df["predicted_label"] = (
        pd.Series(model.predict(dataset.X))
        .apply(lambda x: decoder_dict.get(x, "n/a"))
        .values
    )
    dataset.df["predicted_probability"] = model.predict_proba(dataset.X).max(axis=1)

    columns_to_publish = [
        "element_id",
        "x",
        "y",
        "width",
        "height",
        "predicted_label",
        "predicted_probability",
        "childs",
    ]

    results_df = dataset.df[(dataset.df["predicted_label"] != "n/a")][
        columns_to_publish
    ].copy()
    # # sort in descending order: big controls first
    results_df["sort_key"] = results_df.height * results_df.width
    results_df = results_df.sort_values(by="sort_key", ascending=False)

    #########################
    # current model returns partially non-existing elements' children
    # here we're cleaning it, but it should be corrected on model's side
    def clean_childs():
        elements_ids = list(results_df["element_id"])

        result = []
        for element_childs in list(results_df["childs"]):
            if element_childs:
                cleaned_childs = [
                    item for item in element_childs if item in elements_ids
                ]
                result.append(cleaned_childs)
            else:
                result.append([])
        results_df["childs"] = result

    clean_childs()
    #########################

    if results_df.shape[0] == 0:
        gc.collect()
        return []
    else:
        del model
        gc.collect()
        return results_df.to_dict(orient="records")
