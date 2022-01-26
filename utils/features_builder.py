import os
import re
import numba
import pandas as pd
import numpy as np
import itertools
from sklearn.feature_extraction.text import (
    CountVectorizer,
    TfidfTransformer,
    TfidfVectorizer,
)

# from utils.common import build_elements_dict  # noqa
from utils.common import build_tree_dict

from utils.hidden import build_is_hidden
from tqdm.auto import trange
from utils.config import logger

from sklearn.preprocessing import OneHotEncoder
from scipy.sparse.csr import csr_matrix
from collections import Counter, defaultdict
import pickle
import json

from vars.path_vars import dataset_dict, model_dict
from vars.html5_df_vars import attr_columns, tag_columns, type_columns

prefix = os.getcwd().split("jdi-qasp-ml")[0]

exclude_from_classes_vocab = ["root"]


@numba.jit(forceobj=True)
def get_parents_list(
    tree_dict: dict, element_id: str, paternts_list: list = None
) -> list:
    """
        returns ordered list of parent for a element
        starting from root which is the <html/> tag
    """
    if paternts_list is None:
        paternts_list = []

    parent_id = tree_dict.get(element_id)
    if parent_id is None:
        return paternts_list
    else:
        paternts_list.append(parent_id)
        return get_parents_list(
            tree_dict, element_id=parent_id, paternts_list=paternts_list
        )


def followers_features(
    df: pd.DataFrame, followers_set: set = None, level=0
) -> pd.DataFrame:
    """
        Build feature: "children_tags" and max reverse depth ( depth from leafs) # noqa
        Concatenate all children tag_names into a string filed 'children_tags'
    """
    # get leafs (nodes without children)
    if followers_set is None:
        level = 0
        followers_set = set(df.element_id.values) - set(df.parent_id.values)
        followers_tags_df = (
            df[df.element_id.isin(followers_set)][["parent_id", "tag_name"]]
            .groupby("parent_id")["tag_name"]
            .apply(lambda x: ",".join(x))
            .reset_index()
        )
        followers_tags_dict = dict(followers_tags_df.values)
        df["followers_tags"] = df.element_id.map(followers_tags_dict).fillna("")

        # create max_depth field
        df["max_depth"] = 0
        df.max_depth = df.max_depth + df.element_id.isin(
            set(followers_tags_dict.keys())
        ).astype(int)

        # recursive call
        followers_features(
            df=df, followers_set=set(followers_tags_dict.keys()), level=level + 1
        )

    elif len(followers_set) > 0:
        # print(f'level: {level}')
        followers_tags_df = (
            df[df.element_id.isin(followers_set)][["parent_id", "tag_name"]]
            .groupby("parent_id")["tag_name"]
            .apply(lambda x: ",".join(x))
            .reset_index()
        )
        followers_tags_dict = dict(followers_tags_df.values)
        df["followers_tags"] = (
            df.followers_tags + "," + df.element_id.map(followers_tags_dict).fillna("")
        )

        # increase max_depth
        df.max_depth = df.max_depth + df.element_id.isin(
            set(followers_tags_dict.keys())
        ).astype(int)

        # recursive call
        followers_features(
            df=df, followers_set=set(followers_tags_dict.keys()), level=level + 1
        )

    df["followers_tags"] = df["followers_tags"].apply(
        lambda x: re.sub("\\s+", " ", x.replace(",", " ")).lower().strip()
    )
    return df


def build_tree_features(elements_df: pd.DataFrame) -> pd.DataFrame:
    """
        Walk on elements tree and build tree-features:
        - chilren_tags
        - folloer_counters
    """

    def empty_string():
        return ""

    tree_dict = build_tree_dict(elements_df)

    # Build paths
    followers_counter = Counter()
    # level_dict = defaultdict(int)
    children_tags_dict = defaultdict(empty_string)

    with trange(elements_df.shape[0]) as tbar:
        tbar.set_description("Build tree features")
        for i, r in elements_df.iterrows():
            list_of_parents = get_parents_list(
                tree_dict=tree_dict, element_id=r.element_id
            )
            children_tags_dict[r.parent_id] += r.tag_name.lower() + " "
            # print(list_of_parents)
            # calculate number of followers
            followers_counter.update(list_of_parents)
            tbar.update(1)

    elements_df["children_tags"] = elements_df.element_id.map(
        children_tags_dict
    ).fillna("")
    elements_df["num_followers"] = elements_df.element_id.map(followers_counter)
    return elements_df


class BaseFeaturesBuilder(object):
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.build_features()

    def build_features(self) -> pd.DataFrame:

        build_is_hidden(self.df)
        self.df = followers_features(self.df)
        self.build_children_features()
        self.df = build_tree_features(self.df)
        siblings_dict = self.build_siblings_dict(self.df)
        index_dict = {
            idx: r.element_id
            for idx, r in self.df.iterrows()
            if r.element_id != r.parent_id
        }

        tree_dict = build_tree_dict(self.df)

        elements = self.df.element_id.values  # get siblings for each element

        siblings = [
            self.get_siblings(
                siblings_dict=siblings_dict,
                tree_dict=tree_dict,
                index_dict=index_dict,
                element_id=e,
            )
            for e in elements
        ]

        self.df["upper_sibling"] = [s[0] for s in siblings]
        self.df["lower_sibling"] = [s[1] for s in siblings]
        self.df["siblings"] = siblings

    def build_children_features(self):
        from collections import Counter

        logger.info("select all leafs (nodes which are not parents)")
        leafs_set = set(self.df.element_id.values) - set(self.df.parent_id.values)
        logger.info(f"Leafs set size: {len(leafs_set)} (nodes which have no children)")
        self.df["is_leaf"] = self.df.element_id.apply(
            lambda x: 1 if x in leafs_set else 0
        )

        logger.info("count number of references to leafs")
        num_leafs_dict = Counter(
            self.df[self.df.element_id.isin(leafs_set)].parent_id.values
        )
        logger.info(
            f"Nodes with leafs as children set size: {len(num_leafs_dict)} (nodes which have leafs as children)"
        )
        self.df["num_leafs"] = self.df.element_id.map(num_leafs_dict).fillna(0.0)

        logger.info("count num children for each node")
        num_children_dict = Counter(self.df.parent_id.values)
        logger.info(f"Nodes with children: {len(num_children_dict)}")
        self.df["num_children"] = self.df.element_id.map(num_children_dict).fillna(0.0)

        logger.info("sum of children widths, heights, counts")
        stats_df = self.df.groupby("parent_id").agg(
            {"width": "sum", "height": "sum", "parent_id": "count"}
        )
        stats_df.columns = [
            "sum_children_widths",
            "sum_children_heights",
            "num_children",
        ]
        stats_df.reset_index(inplace=True)

        logger.info("Sum of children widths")
        children_widths_dict = dict(
            stats_df[["parent_id", "sum_children_widths"]].values
        )
        self.df["sum_children_widths"] = self.df.element_id.map(
            children_widths_dict
        ).fillna(0.0)

        logger.info("Sum of children hights")
        children_heights_dict = dict(
            stats_df[["parent_id", "sum_children_heights"]].values
        )
        self.df["sum_children_hights"] = self.df.element_id.map(
            children_heights_dict
        ).fillna(0.0)

    @staticmethod
    def build_siblings_dict(df: pd.DataFrame):
        """
            returns dictionary of nodes which has children
            idx - is an index in the df dataframe

        """

        from collections import defaultdict

        siblings_dict = defaultdict(dict)

        for idx, r in df.iterrows():
            if (r.parent_id == r.element_id) or (r.parent_id is None):
                continue

            p = siblings_dict[r.parent_id]
            p[r.element_id] = idx

        return siblings_dict

    @staticmethod
    def get_siblings(
        siblings_dict: dict, tree_dict: dict, index_dict: dict, element_id: str
    ):
        """
            Returns a pair of siblings (before_sibling, after_sibling)
            for a specified element_id
        """
        parent = tree_dict[element_id]
        siblings = siblings_dict[parent]
        # print('e:', element_id, ', p:', parent, ', s:', siblings)

        idx = siblings.get(element_id)
        if idx is None:  # in the case the element is not found
            return (None, None)

        indices = siblings.values()
        # print(idx, indices)

        up_siblings = [v for v in indices if v < idx]
        dn_siblings = [v for v in indices if v > idx]
        if len(up_siblings) == 0:
            up = None
        else:
            up = max(up_siblings)
        if len(dn_siblings) == 0:
            dn = None
        else:
            dn = min(dn_siblings)

        return index_dict.get(up), index_dict.get(dn)


class SpecialFeaturesBuilder(object):
    """
    Class for calculating special features in case of MUI model
    """

    def __init__(self, df: pd.DataFrame, dataset_type: str = "mui"):

        self.dataset_type = dataset_type
        self.model_path = os.path.join(
            prefix, "jdi-qasp-ml", model_dict.get(dataset_type)
        )
        self.df = df

    def build_features(self):
        # tag_name
        tag_name_sm = self.build_tag_name_feature(colname="tag_name")
        parent_tag_name_sm = self.build_tag_name_feature(colname="tag_name_parent")
        # upsib_tag_name_sm = self.build_tag_name_feature(colname="tag_name_upsib")
        # dnsib_tag_name_sm = self.build_tag_name_feature(colname="tag_name_dnsib")
        logger.info(f"tag_name: {tag_name_sm.shape}")

        # attributes
        attributes_sm = csr_matrix(
            self.build_attributes_feature(colname="attributes").values
        )
        parent_attributes_sm = csr_matrix(
            self.build_attributes_feature(colname="attributes_parent").values
        )
        # upsib_attributes_sm = csr_matrix(
        #     self.build_attributes_feature(colname="attributes_upsib").values
        # )
        # dnsib_attributes_sm = csr_matrix(
        #     self.build_attributes_feature(colname="attributes_dnsib").values
        # )
        logger.info(f"attributes_sm: {attributes_sm.shape}")

        # class
        class_sm = self.build_class_feature(colname="attributes")
        parent_class_sm = self.build_class_feature(colname="attributes_parent")
        # upsib_class_sm = self.build_class_feature(colname="attributes_upsib")
        # dnsib_class_sm = self.build_class_feature(colname="attributes_dnsib")
        logger.info(f"class_sm: {class_sm.shape}")

        # type
        type_sm = self.build_type_feature(colname="attributes")
        parent_type_sm = self.build_type_feature(colname="attributes_parent")
        # upsib_type_sm = self.build_type_feature(colname="attributes_upsib")
        # dnsib_type_sm = self.build_type_feature(colname="attributes_dnsib")
        logger.info(f"type_sm: {type_sm.shape}")

        # role
        role_sm = self.build_role_feature(colname="attributes")
        parent_role_sm = self.build_role_feature(colname="attributes_parent")
        # upsib_role_sm = self.build_role_feature(colname="attributes_upsib")
        # dnsib_role_sm = self.build_role_feature(colname="attributes_dnsib")
        logger.info(f"role_sm: {role_sm.shape}")

        # children & followers tags
        child_tags_sm = self.build_children_tags(colname="children_tags")
        foll_tags_sm = self.build_followers_tags(colname="followers_tags")

        return (
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
        )

    def build_tag_name_feature(self, colname="tag_name") -> csr_matrix:
        """
            colname should be one of ['tag_name', 'tag_name_parent', 'tag_name_up_sibling', 'tag_name_dn_sibling']
        """
        model_file_path = f"{self.model_path}/ohe_tag_name.pkl"
        logger.info(f"used column: {colname}")

        if os.path.exists(model_file_path):
            logger.info(f"loading {model_file_path}")
            with open(model_file_path, "rb") as f:
                model = pickle.load(f)
        else:
            logger.info('Building OHE for "tag_name"')
            tag_name_series = self.df[
                self.df.label_text != "n/a"
            ].tag_name.value_counts()
            tag_name_lst = sorted(list(tag_name_series.index))
            model = OneHotEncoder(handle_unknown="ignore", categories=[tag_name_lst])
            logger.info(f'OHE "tag_name" categories: {model.categories}')
            model.fit(np.expand_dims(self.df.tag_name.values, -1))
            with open(model_file_path, "wb") as f:
                logger.info(f"Saving {model_file_path}")
                pickle.dump(model, f)
                f.flush()

        return model.transform(np.expand_dims(self.df[colname].values, -1))

    def build_attributes_feature(self, colname="attributes") -> pd.DataFrame:
        """
            df must have "attributes" field and we are going
            to extract flag whether the attribute exist or not
            colname should be one from the list [
                'attributes', 'attributes_parent', 'attributes_up_sibling', 'attributes_dn_sibling'
                ]
        """
        dataset_path = os.path.join(
            prefix, "jdi-qasp-ml", dataset_dict.get(self.dataset_type)
        )
        logger.info(f"used column: {colname}")
        attributes = []
        # with open(f"{dataset_path}/EXTRACT_ATTRIBUTES_LIST.pkl", "rb") as f:
        #     EXTRACT_ATTRIBUTES_LIST = pickle.load(f)
        with open(f"{dataset_path}/EXTRACT_ATTRIBUTES_LIST.json", "rb") as f:
            EXTRACT_ATTRIBUTES_LIST = json.load(f)

        with trange(self.df.shape[0]) as bar:
            bar.set_description('Extract "attributes"')

            # create dummy value
            dummy_value = {k: 0 for k in EXTRACT_ATTRIBUTES_LIST}

            for _, r in self.df.iterrows():
                attr = r[colname]
                if type(attr) is dict:
                    d = {}
                    # d['label'] = 1 if r.label_text != 'n/a' else 0
                    for k in EXTRACT_ATTRIBUTES_LIST:
                        v = attr.get(k)
                        if v is not None and v.strip() != "":
                            d[k] = 1
                        else:
                            d[k] = 0
                else:
                    d = dummy_value

                attributes.append(d)
                bar.update(1)

        return pd.DataFrame(attributes)

    def build_class_feature(self, colname="attributes") -> csr_matrix:
        """
            Extract TfIdf features for "class" attribute from a column
            containing attributes ("attributes", "attributes_parent", "attributes_up_sibling"...)
            default columns: "attributes"
        """
        model_tf_file_path = f"{self.model_path}/tfidf_attr_class.pkl"
        logger.info(f"used column: {colname}")

        # if (os.path.exists(model_count_file_path) and os.path.exists(model_tf_file_path)):
        if os.path.exists(model_tf_file_path):
            logger.info(
                "CountVectorizer and TfidfTransformer for class attribute exist. Loading..."
            )
            # with open(model_count_file_path, "rb") as c:
            #     model_cv = pickle.load(file=c)
            with open(model_tf_file_path, "rb") as f:
                model_tf = pickle.load(file=f)
            #             print(f'{model_tf!r}')

        else:
            logger.info(
                "TfIdfVectorizer for class attribute does not exist. Build the one."
            )
            #         if len(set(df.columns).intersection(set(['label', 'label_text']))) != 2:
            #             raise Exception('Cannot prepare CountVectorizer for attribute "class": need labels')

            logger.info(
                "Extract useful attr_class features, 'attributes' column will be used"
            )
            attr_class_series = (
                self.df[self.df.label_text != "n/a"]
                .attributes.apply(lambda x: x.get("class") if x is not None else "")
                .fillna("")
            )
            attr_class_series = (
                attr_class_series.str.replace("-", " ")
                .str.replace(r"[0-9]", "", regex=True)
                .str.lower()
                .str.replace("mui", "")
            )
            model_tf = TfidfVectorizer(ngram_range=(3, 4), analyzer="char_wb").fit(
                attr_class_series.values
            )
            # logger.info(f"NGrams vocabulary: {model_tf.vocabulary_}")

            logger.info(f'Column ["{colname}"] used for tfidf')

            logger.info(f"Saving {model_tf_file_path}")
            with open(model_tf_file_path, "wb") as f:
                pickle.dump(model_tf, f)
                f.flush()

        attr_class_series = (
            self.df[colname]
            .apply(lambda x: None if type(x) is not dict else x.get("class"))
            .fillna("")
        )
        attr_class_series = (
            attr_class_series.str.replace("-", " ")
            .str.replace(r"[0-9]", "", regex=True)
            .str.lower()
            .str.replace("mui", "")
        )

        class_sm = model_tf.transform(attr_class_series.values)

        return class_sm

    def build_type_feature(self, colname="attributes") -> csr_matrix:
        model_file_path = f"{self.model_path}/ohe_type.pkl"
        logger.info(f"used column: {colname}")

        if os.path.exists(model_file_path):
            logger.info(f"loading {model_file_path}")
            with open(model_file_path, "rb") as f:
                ohe = pickle.load(f)
        else:
            logger.info('Building OHE for "type"')
            # We'll use only target's data
            attr_type_series = (
                self.df[self.df.label_text != "n/a"]
                .attributes.apply(
                    lambda x: None if type(x) is not dict else x.get("type")
                )
                .fillna("")
            )
            ohe = OneHotEncoder(handle_unknown="ignore").fit(
                np.expand_dims(attr_type_series.values, -1)
            )
            logger.info(f'OHE "type" categories: {ohe.categories}')
            with open(model_file_path, "wb") as f:
                logger.info(f"Saving {model_file_path}")
                pickle.dump(ohe, f)
                f.flush()

        attr_type_series = (
            self.df[colname]
            .apply(lambda x: None if type(x) is not dict else x.get("type"))
            .fillna("")
        )

        return ohe.transform(np.expand_dims(attr_type_series, -1))

    def build_role_feature(self, colname="attributes") -> csr_matrix:
        model_file_path = f"{self.model_path}/ohe_role.pkl"
        logger.info(f"used column: {colname}")

        if os.path.exists(model_file_path):
            logger.info(f"loading {model_file_path}")
            with open(model_file_path, "rb") as f:
                ohe = pickle.load(f)
        else:
            logger.info('Building OHE for "role"')
            # We'll use only target's data
            attr_role_series = (
                self.df[self.df.label_text != "n/a"]
                .attributes.apply(
                    lambda x: None if type(x) is not dict else x.get("role")
                )
                .fillna("")
            )
            ohe = OneHotEncoder(handle_unknown="ignore").fit(
                np.expand_dims(attr_role_series.values, -1)
            )
            logger.info(f'OHE "role" categories: {ohe.categories}')
            with open(model_file_path, "wb") as f:
                logger.info(f"Saving {model_file_path}")
                pickle.dump(ohe, f)
                f.flush()

        attr_role_series = (
            self.df[colname]
            .apply(lambda x: None if type(x) is not dict else x.get("role"))
            .fillna("")
        )

        return ohe.transform(np.expand_dims(attr_role_series, -1))

    def build_children_tags(self, colname="children_tags") -> csr_matrix:
        model_count_path = f"{self.model_path}/count_children_tags.pkl"
        model_tf_path = f"{self.model_path}/tfidf_children_tags.pkl"
        logger.info(f"used column: {colname}")

        if os.path.exists(model_count_path) and os.path.exists(model_tf_path):
            logger.info(
                "CountVectorizer and TfidfTransformer for children tags exist. Loading..."
            )
            with open(model_count_path, "rb") as c:
                model_cv = pickle.load(file=c)
            with open(model_tf_path, "rb") as f:
                model_tf = pickle.load(file=f)

            child_tags_series = self.df[colname].fillna("")
            child_tags_series = child_tags_series.apply(
                lambda x: x.strip() if x != "" else x
            )
            child_sm = model_cv.transform(child_tags_series.values)
            child_sm = model_tf.transform(child_sm)

        else:
            logger.info(
                "TfIdfVectorizer for children tags does not exist. Build the one."
            )

            logger.info(
                "Extract useful child_tags features, 'children_tags' column will be used"
            )
            child_tags_series = self.df[colname].fillna("")
            child_vocab = list(
                itertools.chain.from_iterable(
                    child_tags_series.apply(lambda x: x.split(sep=" "))
                )
            )
            child_vocab = list(set(child_vocab))
            child_vocab = sorted(
                [v for v in child_vocab if re.match(r"^[a-z][a-z]+$", v)]
            )

            child_cv = CountVectorizer(vocabulary=child_vocab)
            child_sm = child_cv.fit_transform(child_tags_series.values)

            logger.info(f'Column ["{colname}"] used for tfidf')

            model = TfidfTransformer()
            child_sm = model.fit_transform(child_sm)

            logger.info(
                f"Saving {model_count_path}, vocabulary length: {len(child_cv.vocabulary_)}"
            )
            logger.info(f"Saving {model_tf_path}")
            with open(model_count_path, "wb") as c:
                pickle.dump(child_cv, c)
                c.flush()
            with open(model_tf_path, "wb") as f:
                pickle.dump(model, f)
                f.flush()

        return child_sm

    def build_followers_tags(self, colname="followers_tags") -> csr_matrix:
        model_count_path = f"{self.model_path}/count_followers_tags.pkl"
        model_tf_path = f"{self.model_path}/tfidf_followers_tags.pkl"
        logger.info(f"used column: {colname}")

        if os.path.exists(model_count_path) and os.path.exists(model_tf_path):
            logger.info(
                "CountVectorizer and TfidfTransformer for followers tags exist. Loading..."
            )
            with open(model_count_path, "rb") as c:
                model_cv = pickle.load(file=c)
            with open(model_tf_path, "rb") as f:
                model_tf = pickle.load(file=f)

            followers_tags_series = self.df[colname].fillna("")
            followers_tags_series = followers_tags_series.apply(
                lambda x: x.strip() if x != "" else x
            )
            followers_sm = model_cv.transform(followers_tags_series.values)
            followers_sm = model_tf.transform(followers_sm)

        else:
            logger.info(
                "CountVectorizer and TfIdfTransformer for followers tags do not exist. Build them."
            )

            logger.info(
                "Extract useful child_tags features, 'followers_tags' column will be used"
            )
            followers_tags_series = self.df[colname].fillna("")
            followers_vocab = list(
                itertools.chain.from_iterable(
                    followers_tags_series.apply(lambda x: x.split(sep=" "))
                )
            )
            followers_vocab = list(set(followers_vocab))
            followers_vocab = sorted(
                [v for v in followers_vocab if re.match(r"^[a-z][a-z]+$", v)]
            )

            followers_cv = CountVectorizer(vocabulary=followers_vocab)
            followers_sm = followers_cv.fit_transform(followers_tags_series.values)

            logger.info(f'Column ["{colname}"] used for tfidf')

            model = TfidfTransformer()
            followers_sm = model.fit_transform(followers_sm)

            logger.info(
                f"Saving {model_count_path}, vocabulary length: {len(followers_cv.vocabulary_)}"
            )
            logger.info(f"Saving {model_tf_path}")
            with open(model_count_path, "wb") as c:
                pickle.dump(followers_cv, c)
                c.flush()
            with open(model_tf_path, "wb") as f:
                pickle.dump(model, f)
                f.flush()

        return followers_sm


class HTML5SpecialFeaturesBuilder(object):
    """
    Class for calculating special features in case of html5 model
    """

    def __init__(self, df: pd.DataFrame, dataset_type="html5"):
        self.dataset_type = "html5"
        self.df = df

    def build_features(self):

        # make column with special child parameters (for radiobuttongroup and checklist uses only)
        self.df["is_checkbox_in_childs"] = self.df["childs_types"].apply(
            lambda x: 1 if "checkbox" in x else 0
        )
        self.df["is_radio_in_childs"] = self.df["childs_types"].apply(
            lambda x: 1 if "radio" in x else 0
        )

        # drop unneded features
        self.reduce_features(
            [
                "element_id",
                "tag_name",
                "attributes_list",
                "type",
                "is_checkbox_in_childs",
                "is_radio_in_childs",
            ]
        )

        self.build_onehot_features()

        return self.df[
            self.tag_columns
            + self.attr_columns
            + self.type_columns
            + ["is_checkbox_in_childs", "is_radio_in_childs"]
        ]

    def reduce_features(self, feature_list):
        self.df = self.df[feature_list].copy()

    def build_onehot_features(self):
        for col in attr_columns:
            self.df.loc[:, "attr_" + col] = (
                self.df.loc[:, "attributes_list"]
                .apply(lambda x: 1 if col in x else 0)
                .values
            )

        for col in tag_columns:
            self.df.loc[:, "tag_" + col] = (
                self.df.loc[:, "tag_name"].apply(lambda x: 1 if col == x else 0).values
            )

        for col in type_columns:
            self.df.loc[:, "type_" + col] = (
                self.df.loc[:, "type"].apply(lambda x: 1 if col == x else 0).values
            )

        self.attr_columns = ["attr_" + col for col in attr_columns]

        self.tag_columns = ["tag_" + col for col in tag_columns]

        self.type_columns = ["type_" + col for col in type_columns]

        self.df.set_index(self.df.element_id, inplace=True)


logger.info("feature_bilder module is loaded...")
