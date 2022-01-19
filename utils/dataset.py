import os

import pandas as pd
import numpy as np
import logging
from tqdm.auto import trange
from utils.dataset_collector import MUI_DatasetCollector, HTML5_DatasetCollector
from utils.features_builder import BaseFeaturesBuilder

from utils.labels import assign_labels

from torch.utils.data import Dataset
from glob import glob
from utils.config import logger
from vars.path_vars import dataset_dict

prefix = os.getcwd().split("jdi-qasp-ml")[0]


def rebalance(y: np.ndarray, classes_path):
    """
    Function for rabalancing dataset to increase number of rare objects
    """
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
    """
    Class for creating dataset pytorch instance 
    """

    def __init__(
        self,
        dataset_type: str = "mui",
        datasets_list: list = None,
        rebalance_and_shuffle: bool = False,
    ):

        super(JDNDataset, self).__init__()
        self.dataset_type = dataset_type
        self.datasets_list = datasets_list
        self.rebalance_and_suffle = rebalance_and_shuffle

        self.dataset_path = dataset_dict.get(dataset_type)
        self.classes_path = os.path.join(
            prefix, "jdi-qasp-ml", f"{self.dataset_path}/classes.txt"
        )
        self.df_path = os.path.join(prefix, "jdi-qasp-ml", f"{self.dataset_path}/df")

        self.get_files()

    def get_files(self):

        with open(self.classes_path, "r") as f:
            lines = f.readlines()
            self.classes_dict = {v.strip(): i for i, v in enumerate(lines)}
            self.classes_reverse_dict = {i: v.strip() for i, v in enumerate(lines)}

        if self.datasets_list is None:
            logger.info("Will use all available datasets")
            self.ds_files = glob(f"{self.df_path}/*.pkl")
        else:
            self.ds_files = [(f"{self.df_path}/{fn}.pkl") for fn in self.datasets_list]

    def check_for_duplicates(self):

        logger.info("Check for duplicates...")
        if self.df.element_id.nunique() != self.df.shape[0]:
            logger.fatal("There are duplicates in the dataset")
            raise Exception("There are duplicates in the dataset")
        logger.info("Check for duplicates is OK")

    def __getitem__(self, idx):
        return self.X[self.indices[idx]], self.y[self.indices[idx]]

    def __len__(self):
        return self.indices.shape[0]


class MUI_JDNDataset(JDNDataset):
    """
    Class for creating dataset pytorch instance in case of MUI model 
    """

    def __init__(
        self,
        dataset_type: str = "mui",
        datasets_list: list = None,
        rebalance_and_shuffle: bool = False,
    ):
        super().__init__(
            dataset_type=dataset_type,
            datasets_list=datasets_list,
            rebalance_and_shuffle=rebalance_and_shuffle,
        )

        self.build_primari_features_and_concatenate()
        self.check_for_duplicates()
        self.build_secondary_features()

    def build_primari_features_and_concatenate(self):
        df_list = []

        logger.setLevel(logging.ERROR)
        with trange(len(self.ds_files)) as bar:
            for df_file_path in self.ds_files:
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
                    df = assign_labels(df=df, classes_file_path=self.classes_path)
                    df_list.append(df)
                bar.update(1)

        logger.setLevel(logging.DEBUG)

        self.df = pd.concat(df_list)
        logger.info(f"self.df.shape: {self.df.shape}")

    def build_secondary_features(self):

        self.X, self.y = MUI_DatasetCollector(
            self.df, self.dataset_type
        ).collect_dataset()

        if self.rebalance_and_suffle:
            self.indices = np.array(rebalance(self.y, self.classes_path))
        else:
            self.indices = np.array([i for i in range(len(self.y))])


class HTML5_JDNDataset(JDNDataset):
    """
    Class for creating dataset pytorch instance in case of HTML5 model 
    """

    def __init__(
        self,
        dataset_type: str = "html5",
        datasets_list: list = None,
        rebalance_and_shuffle: bool = False,
    ):
        super().__init__(
            dataset_type=dataset_type,
            datasets_list=datasets_list,
            rebalance_and_shuffle=rebalance_and_shuffle,
        )

        self.build_primari_features_and_concatenate()
        self.check_for_duplicates()
        self.build_secondary_features()

    def build_primari_features_and_concatenate(self):
        df_list = []

        logger.setLevel(logging.ERROR)
        with trange(len(self.ds_files)) as bar:
            for df_file_path in self.ds_files:
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
                    df = self.build_additional_features(df)
                    df = assign_labels(df=df, classes_file_path=self.classes_path)
                    df_list.append(df)
                bar.update(1)

        logger.setLevel(logging.DEBUG)

        self.df = pd.concat(df_list)
        self.df.set_index(self.df.element_id, inplace=True)
        logger.info(f"self.df.shape: {self.df.shape}")

    def build_secondary_features(self):

        logger.info("Calculating features...")
        self.X, self.y = HTML5_DatasetCollector(
            self.df, self.dataset_type
        ).collect_dataset()
        logger.info("Features have calculated succesfully!")
        if self.rebalance_and_suffle:
            self.indices = np.array(rebalance(self.y, self.classes_path))
        else:
            self.indices = np.array([i for i in range(len(self.y))])

    @staticmethod
    def build_additional_features(df):

        # make column with list of attributes
        df["attributes_list"] = df.attributes.apply(
            lambda x: "" if x is None else " ".join(list(x.keys()))
        )
        # make column with type attribute
        df["type"] = df.attributes.apply(
            lambda x: None
            if (None if x is None else x.get("type")) is None
            else x.get("type")
        ).fillna("n/a")

        par_childs = {
            par: list(df[df.parent_id == par].element_id.unique())
            for par in df.parent_id.unique()
        }
        df["childs"] = df["element_id"].apply(lambda x: par_childs.get(x))
        df["childs_types"] = df["childs"].apply(
            lambda l: [None]
            if l is None
            else [
                df[df.element_id == i].type.iloc[0]
                if df[df.element_id == i].type.iloc[0] != "n/a"
                else None
                for i in l
            ]
        )

        return df


logger.info("dataset module is loaded...")
