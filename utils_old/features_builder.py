import os, sys
import re
import numba
import pandas as pd
import numpy as np

from .common import build_elements_dict  # noqa
from .common import build_tree_dict
from .common import to_yolo
from .hidden import build_is_hidden
from tqdm.auto import trange
from .config import logger

# from scipy.sparse import csc_matrix, csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse.csr import csr_matrix
import pickle

prefix = os.getcwd().split("jdi-qasp-ml")[0]
sys.path.append(os.path.join(prefix, "jdi-qasp-ml"))

model_path = os.path.join(prefix, "jdi-qasp-ml", "Old_model/model")


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


# # @numba.jit
# def build_to_yolo(df: pd.DataFrame, img_width: int, img_heght: int):
#     return np.round(np.array(
#         [to_yolo(r.label, r.x, r.y, r.width, r.height, img_width, img_heght)
#          for _, r in df.iterrows()]
#     ), 6)


@numba.jit(forceobj=True)
def build_to_yolo(df: pd.DataFrame, img_width: int, img_heght: int):
    lst = [
        to_yolo(r.label, r.x, r.y, r.width, r.height, img_width, img_heght)
        for _, r in df.iterrows()
    ]
    return lst


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


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
        Enrich dataset with features.
        The df:pd.DataFrame must have columns: ['element_id', 'parent_id', 'x', 'y', 'width', 'height']
    """

    # build IS_HIDDEN feature
    build_is_hidden(df)

    siblings_dict = build_siblings_dict(df)
    index_dict = {
        idx: r.element_id for idx, r in df.iterrows() if r.element_id != r.parent_id
    }

    # elements_dict = build_elements_dict(df)
    tree_dict = build_tree_dict(df)

    elements = df.element_id.values  # get siblings for each element

    siblings = [
        get_siblings(
            siblings_dict=siblings_dict,
            tree_dict=tree_dict,
            index_dict=index_dict,
            element_id=e,
        )
        for e in elements
    ]

    df["upper_sibling"] = [s[0] for s in siblings]
    df["lower_sibling"] = [s[1] for s in siblings]
    df["siblings"] = siblings

    return df


EXTRACT_ATTRIBUTES_LIST = [
    "aria-invalid",
    "aria-haspopup",
    "aria-expanded",
    "aria-required",
    "aria-disabled",
    "aria-selected",
    "aria-describedby",
    "aria-controls",
    "aria-invalid",
    "placeholder",
    "value",
    "for",
    "onclick",
    "target",
    # 'role',
    # 'type',
    # 'class',
    "id",
    "name",
    # 'href',  ## I think it highly correlates with <A> attribute
    "min",
    "max",
]


def build_attributes_feature(df: pd.DataFrame, colname="attributes") -> pd.DataFrame:
    """
        df must have "attributes" field and we are going
        to extract flag whether the attribute exist or not
        colname should be one from the list [
            'attributes', 'attributes_parent', 'attributes_up_sibling', 'attributes_dn_sibling'
            ]
    """
    logger.info(f"used column: {colname}")
    attributes = []

    with trange(df.shape[0]) as bar:
        bar.set_description('Extract "attributes"')

        # create dummy value
        dummy_value = {k: 0 for k in EXTRACT_ATTRIBUTES_LIST}

        for _, r in df.iterrows():
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


def build_class_feature(df: pd.DataFrame, colname="attributes") -> csr_matrix:
    """
        Extract TfIdf features for "class" attribute from a column
        containing attributes ("attributes", "attributes_parent", "attributes_up_sibling"...)
        default columns: "attributes"
    """
    model_file_path = f"{model_path}/tfidf_attr_class.pkl"
    logger.info(f"used column: {colname}")

    if os.path.exists(model_file_path):
        logger.info("TfIdfVectorizer for class attribute exists. Loaging...")
        with open(model_file_path, "rb") as f:
            model = pickle.load(file=f)
        attr_class_series = (
            df[colname]
            .apply(lambda x: None if type(x) is not dict else x.get("class"))
            .fillna("")
        )

    else:
        logger.info(
            "TfIdfVectorizer for class attribute does not exist. Build the one."
        )
        if len(set(df.columns).intersection(set(["label", "label_text"]))) != 2:
            raise Exception(
                'Cannot prepare CountVectorizer for attribute "class": need labels'
            )

        logger.info(
            "Extract useful attr_class features, 'attributes' column will be used"
        )
        attr_class_series = (
            df[df.label_text != "n/a"]
            .attributes.apply(lambda x: None if type(x) is not dict else x.get("class"))
            .fillna("")
        )

        class_cv = CountVectorizer()
        class_cv.fit(attr_class_series.values)
        # filter out class names:  length is at least 2 characters and only letters
        vocabulary = sorted(
            [v for v in class_cv.vocabulary_.keys() if re.match(r"^[a-z][a-z]+$", v)]
        )

        logger.info(f'Column ["{colname}"] used for tfidf')
        attr_class_series = (
            df[colname]
            .apply(lambda x: None if type(x) is not dict else x.get("class"))
            .fillna("")
        )
        model = TfidfVectorizer(vocabulary=vocabulary)  # CountVectorizer?
        model.fit(attr_class_series.values)
        logger.info(f"Saving {model_file_path}, vocabulary length: {len(vocabulary)}")
        with open(model_file_path, "wb") as f:
            pickle.dump(model, f)
            f.flush()

    return model.transform(attr_class_series.values)


def build_tag_name_feature(df: pd.DataFrame, colname="tag_name") -> csr_matrix:
    """
        colname should be one of ['tag_name', 'tag_name_parent', 'tag_name_up_sibling', 'tag_name_dn_sibling']
    """
    model_file_path = f"{model_path}/ohe_tag_name.pkl"
    logger.info(f"used column: {colname}")

    if os.path.exists(model_file_path):
        logger.info(f"loading {model_file_path}")
        with open(model_file_path, "rb") as f:
            model = pickle.load(f)
    else:
        logger.info('Building OHE for "tag_name"')
        tag_name_series = df[df.label_text != "n/a"].tag_name.value_counts()
        tag_name_lst = sorted(list(tag_name_series.index))
        model = OneHotEncoder(handle_unknown="ignore", categories=[tag_name_lst])
        logger.info(f'OHE "tag_name" categories: {model.categories}')
        model.fit(np.expand_dims(df.tag_name.values, -1))
        with open(model_file_path, "wb") as f:
            logger.info(f"Saving {model_file_path}")
            pickle.dump(model, f)
            f.flush()

    return model.transform(np.expand_dims(df[colname].values, -1))


def build_role_feature(df: pd.DataFrame, colname="attributes") -> csr_matrix:
    model_file_path = f"{model_path}/ohe_role.pkl"
    logger.info(f"used column: {colname}")

    if os.path.exists(model_file_path):
        logger.info(f"loading {model_file_path}")
        with open(model_file_path, "rb") as f:
            ohe = pickle.load(f)
    else:
        logger.info('Building OHE for "role"')
        # We'll use only target's data
        attr_role_series = (
            df[df.label_text != "n/a"]
            .attributes.apply(lambda x: None if type(x) is not dict else x.get("role"))
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
        df[colname]
        .apply(lambda x: None if type(x) is not dict else x.get("role"))
        .fillna("")
    )

    return ohe.transform(np.expand_dims(attr_role_series, -1))


def build_type_feature(df: pd.DataFrame, colname="attributes") -> csr_matrix:
    model_file_path = f"{model_path}/ohe_type.pkl"
    logger.info(f"used column: {colname}")

    if os.path.exists(model_file_path):
        logger.info(f"loading {model_file_path}")
        with open(model_file_path, "rb") as f:
            ohe = pickle.load(f)
    else:
        logger.info('Building OHE for "type"')
        # We'll use only target's data
        attr_type_series = (
            df[df.label_text != "n/a"]
            .attributes.apply(lambda x: None if type(x) is not dict else x.get("type"))
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
        df[colname]
        .apply(lambda x: None if type(x) is not dict else x.get("type"))
        .fillna("")
    )

    return ohe.transform(np.expand_dims(attr_type_series, -1))


logger.info("feature_bilder module is loaded...")

