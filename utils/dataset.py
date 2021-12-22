import os

import pandas as pd
import numpy as np
import logging
from tqdm.auto import trange
from utils.dataset_collector import collect_dataset
from utils.features_builder import BaseFeaturesBuilder

from utils.labels import assign_labels

from torch.utils.data import Dataset
from glob import glob
from utils.config import logger
from vars.path_vars import dataset_dict

prefix = os.getcwd().split("jdi-qasp-ml")[0]


def rebalance(y: np.ndarray, classes_path):
    logger.info("Rebalance dataset")

    with open(classes_path, "r") as f:
        decoder_dict = {i: v.strip() for i, v in enumerate(f.readlines())}

    proportion_df = pd.DataFrame(
        [
            {
                "label": i,
                "label_text": decoder_dict[i],
                "cnt": np.where(y == i)[0].shape[0],
            }
            for i in range(0, len(decoder_dict))
        ]
    )

    labels_cnt = (
        proportion_df[proportion_df.label_text != "n/a"][["cnt"]].sum().values[0]
    )
    na_label_cnt = proportion_df[proportion_df.label_text == "n/a"].cnt.values[0]
    logger.info(f'"n/a" count: {na_label_cnt}, labels count: {labels_cnt}')

    proportion_df["ratio"] = proportion_df.apply(
        lambda r: na_label_cnt // r.cnt // 15
        if (r.label_text != "n/a") and (r.cnt > 0)
        else 1,
        axis=1,
    )

    proportion_df["cnt_rebalanced"] = proportion_df.ratio * proportion_df.cnt
    # display(proportion_df)

    indices = []
    for i, r in proportion_df.iterrows():
        lst = np.where(y == r.label)[0].tolist()
        for _ in range(r.ratio):
            indices.extend(lst)

    np.random.shuffle(indices)
    logger.info(f"Rebalanced and shuffled indices: {len(indices)}")

    return indices


class JDNDataset(Dataset):
    def __init__(
        self,
        dataset_type: str = "mui",
        datasets_list: list = None,
        rebalance_and_shuffle: bool = False,
    ):

        super(JDNDataset, self).__init__()
        self.rebalance_and_suffle = rebalance_and_shuffle

        dataset_path = dataset_dict.get(dataset_type)
        classes_path = os.path.join(
            prefix, "jdi-qasp-ml", f"{dataset_path}/classes.txt"
        )
        df_path = os.path.join(prefix, "jdi-qasp-ml", f"{dataset_path}/df")

        with open(classes_path, "r") as f:
            lines = f.readlines()
            self.classes_dict = {v.strip(): i for i, v in enumerate(lines)}
            self.classes_reverse_dict = {i: v.strip() for i, v in enumerate(lines)}

        if datasets_list is None:
            logger.info("Will use all available datasets")
            ds_files = glob(f"{df_path}/*.pkl")
        else:
            ds_files = [(f"{df_path}/{fn}.pkl") for fn in datasets_list]

        df_list = []

        logger.setLevel(logging.ERROR)
        with trange(len(ds_files)) as bar:
            for df_file_path in ds_files:
                if not os.path.exists(df_file_path):
                    logger.error(f"File: {df_file_path} does not extst")
                else:
                    bar.set_postfix_str(f"{df_file_path}")
                    #                     df = pd.read_parquet(df_file_path)
                    df = pd.read_pickle(df_file_path)
                    df["label_text"] = df.attributes.apply(
                        lambda x: x.get("data-label") if x is not None else "n/a"
                    ).fillna("n/a")
                    df = BaseFeaturesBuilder(df).df
                    df = assign_labels(df=df)
                    df_list.append(df)
                bar.update(1)

        logger.setLevel(logging.DEBUG)

        self.df = pd.concat(df_list)
        logger.info(f"self.df.shape: {self.df.shape}")

        logger.info("Check for duplicates...")
        if self.df.element_id.nunique() != self.df.shape[0]:
            logger.fatal("There are duplicates in the dataset")
            raise Exception("There are duplicates in the dataset")
        logger.info("Check for duplicates is OK")

        self.X, self.y = collect_dataset(self.df, dataset_type)

        if self.rebalance_and_suffle:
            self.indices = np.array(rebalance(self.y, classes_path))
        else:
            self.indices = np.array([i for i in range(len(self.y))])

    def __getitem__(self, idx):
        return self.X[self.indices[idx]], self.y[self.indices[idx]]

    def __len__(self):
        return self.indices.shape[0]


logger.info("dataset module is loaded...")
