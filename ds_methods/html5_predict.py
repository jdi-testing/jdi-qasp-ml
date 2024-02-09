import datetime as dt
import gc
import json
import logging
import os
import pickle

import pandas as pd
from async_lru import alru_cache

from app import (UPLOAD_DIRECTORY, html5_classes_path, html5_df_path,
                 html5_model)
from app.selenium_app import get_element_id_to_is_displayed_mapping
from utils.dataset import HTML5_JDNDataset

logger = logging.getLogger("jdi-qasp-ml")


@alru_cache(maxsize=32)
async def html5_predict_elements(body):
    body_str = body.decode("utf-8")
    body_json = json.loads(body_str)
    elements_json = body_json.get("elements", [])
    document_json = body_json.get("document", "")

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

    dataset.df["predicted_probability"] = model.predict_proba(dataset.X).max(
        axis=1
    )

    columns_to_publish = [
        "element_id",
        "predicted_label",
        "childs",
        "displayed",
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
        result = results_df[columns_to_publish].to_dict(orient="records")

        logger.info("Determining visibility locators")
        element_id_to_is_displayed_map = get_element_id_to_is_displayed_mapping(document_json)
        for element in result:
            element["is_shown"] = element_id_to_is_displayed_map.get(element["element_id"], None)
        return result
