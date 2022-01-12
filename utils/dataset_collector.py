import pandas as pd
import numpy as np
from utils.config import logger
from scipy.sparse.csr import csr_matrix
from scipy.sparse import hstack


from utils.features_builder import SpecialFeaturesBuilder, HTML5SpecialFeaturesBuilder

from vars.path_vars import dataset_dict, model_dict


COLS = ["element_id", "tag_name", "attributes", "displayed", "is_hidden"]

TARGET_PARENT_COLUMNS = [
    "parent_id",
    "tag_name_parent",
    "attributes_parent",
    "displayed_parent",
    "is_hidden_parent",
]

TARGET_UP_SIBLING_COLUMNS = [
    "upper_sibling",
    "tag_name_upsib",
    "attributes_upsib",
    "displayed_upsib",
    "is_hidden_upsib",
]

TARGET_DN_SIBLING_COLUMNS = [
    "lower_sibling",
    "tag_name_dnsib",
    "attributes_dnsib",
    "displayed_dnsib",
    "is_hidden_dnsib",
]


class DatasetCollector(object):
    def __init__(self, df: pd.DataFrame, dataset_type="mui"):
        self.df = df
        self.dataset_type = dataset_type
        self.prepare_df()

    def prepare_df(self):
        df_parent = self.df[COLS].copy()
        df_parent.columns = TARGET_PARENT_COLUMNS

        upsib_df = self.df[COLS].copy()
        upsib_df.columns = TARGET_UP_SIBLING_COLUMNS

        dnsib_df = self.df[COLS].copy()
        dnsib_df.columns = TARGET_DN_SIBLING_COLUMNS

        self.dataset_df = self.df.merge(df_parent, on="parent_id", how="left")
        self.dataset_df = self.dataset_df.merge(
            upsib_df, on="upper_sibling", how="left"
        )
        self.dataset_df = self.dataset_df.merge(
            dnsib_df, on="lower_sibling", how="left"
        )

        self.y = self.df.label.values


class MUI_DatasetCollector(DatasetCollector):
    def __init__(self, df: pd.DataFrame, dataset_type="mui"):
        super().__init__(df, dataset_type=dataset_type)

    def collect_dataset(self) -> csr_matrix:
        (
            attributes_sm,
            parent_attributes_sm,
            # upsib_attributes_sm,
            # dnsib_attributes_sm,
            class_sm,
            parent_class_sm,
            # upsib_class_sm,
            # dnsib_class_sm,
            tag_name_sm,
            parent_tag_name_sm,
            # upsib_tag_name_sm,
            # dnsib_tag_name_sm,
            type_sm,
            parent_type_sm,
            # upsib_type_sm,
            # dnsib_type_sm,
            role_sm,
            parent_role_sm,
            # upsib_role_sm,
            # dnsib_role_sm,
            child_tags_sm,
            foll_tags_sm,
        ) = SpecialFeaturesBuilder(self.dataset_df, self.dataset_type).build_features()

        X = np.array(
            hstack(
                [
                    attributes_sm,
                    parent_attributes_sm,
                    # upsib_attributes_sm,
                    # dnsib_attributes_sm,
                    class_sm,
                    parent_class_sm,
                    # upsib_class_sm,
                    # dnsib_class_sm,
                    tag_name_sm,
                    parent_tag_name_sm,
                    # upsib_tag_name_sm,
                    # dnsib_tag_name_sm,
                    type_sm,
                    parent_type_sm,
                    # upsib_type_sm,
                    # dnsib_type_sm,
                    role_sm,
                    parent_role_sm,
                    # upsib_role_sm,
                    # dnsib_role_sm,
                    child_tags_sm,
                    foll_tags_sm,
                    self.dataset_df.num_followers.fillna(False)
                    .astype(int)
                    .values.reshape(-1, 1),
                    self.dataset_df.is_leaf.fillna(False)
                    .astype(int)
                    .values.reshape(-1, 1),
                    self.dataset_df.num_leafs.fillna(False)
                    .astype(int)
                    .values.reshape(-1, 1),
                    self.dataset_df.num_children.fillna(False)
                    .astype(int)
                    .values.reshape(-1, 1),
                    self.dataset_df.sum_children_widths.fillna(False)
                    .astype(int)
                    .values.reshape(-1, 1),
                    self.dataset_df.sum_children_hights.fillna(False)
                    .astype(int)
                    .values.reshape(-1, 1),
                    self.dataset_df.max_depth.astype(int).values.reshape(-1, 1),
                    self.dataset_df.displayed.astype(int).values.reshape(-1, 1),
                    self.dataset_df.displayed_parent.fillna(False)
                    .astype(int)
                    .values.reshape(-1, 1),
                    # dataset_df.displayed_upsib.fillna(False)
                    # .astype(int)
                    # .values.reshape(-1, 1),
                    # dataset_df.displayed_dnsib.fillna(False)
                    # .astype(int)
                    # .values.reshape(-1, 1),
                    self.dataset_df.is_hidden.fillna(1.0).values.reshape(-1, 1),
                    self.dataset_df.is_hidden_parent.fillna(1.0).values.reshape(-1, 1),
                    # dataset_df.is_hidden_upsib.fillna(1.0).values.reshape(-1, 1),
                    # dataset_df.is_hidden_dnsib.fillna(1.0).values.reshape(-1, 1),
                ]
            ).todense()
        )  # I hope we have enougth RAM
        # pd.DataFrame(X, columns=[f"{i}" for i in range(X.shape[1])]).to_parquet(
        #     "/Users/Mikhail_Bulgakov/GitRepo/jdi-qasp-ml/MUI_model/tmp/dataframe_X.parquet"
        # )
        # pd.DataFrame(y, columns=["y"]).to_parquet(
        #     "/Users/Mikhail_Bulgakov/GitRepo/jdi-qasp-ml/MUI_model/tmp/dataframe_y.parquet"
        # )
        logger.info(f"X: {X.shape}")
        return X.astype(np.float32), self.y


class HTML5_DatasetCollector(DatasetCollector):
    def __init__(self, df: pd.DataFrame, dataset_type="html5"):
        super().__init__(df, dataset_type=dataset_type)

    def collect_dataset(self) -> csr_matrix:
        self.dataset_df = HTML5SpecialFeaturesBuilder(
            self.dataset_df, self.dataset_type
        ).build_features()

        logger.info(f"X: {self.dataset_df.shape}")
        return self.dataset_df, self.y
