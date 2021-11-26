import os, sys

prefix = os.getcwd().split("jdi-qasp-ml")[0]
sys.path.append(os.path.join(prefix, "jdi-qasp-ml"))

import pandas as pd
import numpy as np
from utils.config import logger

from tqdm.auto import tqdm
from collections import defaultdict


classes_path = os.path.join(prefix, "jdi-qasp-ml", "data/mui_dataset/classes.txt")


def assign_labels(
    df: pd.DataFrame, classes_file_path: str = classes_path, verbose=False
) -> pd.DataFrame:

    with open(classes_file_path, "r") as f:
        lines = f.readlines()
        encoder_dict = {line.strip(): i for i, line in enumerate(lines)}
        logger.info(str(encoder_dict))
        decoder_dict = {v: k for k, v in encoder_dict.items()}

    if len(encoder_dict) != len(decoder_dict):
        msg = f"There are duplicate key/values in the {classes_file_path}"
        logger.fatal(msg)
        raise Exception(msg)

    def labels(label_text, encoder_dict):
        encoded_label = encoder_dict[label_text]
        return encoded_label

    vec_labels = np.vectorize(labels, excluded=["encoder_dict"])

    def remove_unused_classes(label_text):
        if label_text not in encoder_dict.keys():
            return "n/a"
        else:
            return label_text

    df["label_text"] = df["label_text"].apply(remove_unused_classes)
    # print(
    #     "!!!!!!!!!!!!! LABELS:",
    #     df["label_text"].unique(),
    #     len(df["label_text"].unique()),
    # )
    df["label"] = vec_labels(df["label_text"], encoder_dict)
    # remove duplicates
    df = df.sort_values(by=["element_id", "parent_id"])
    df = df[~df[["element_id", "parent_id"]].duplicated(keep="last")].copy()

    return df
