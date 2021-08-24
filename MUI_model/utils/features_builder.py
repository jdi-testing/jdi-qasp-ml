import os
import re
import numba
import pandas as pd
import numpy as np

# from .dataset import build_children_features
# from .dataset import followers_features 
# from .dataset import build_tree_features
# from utils.common import build_elements_dict  # noqa
from utils.common import build_tree_dict

from utils.hidden import build_is_hidden
from tqdm.auto import trange
from utils.config import logger

# from scipy.sparse import csc_matrix, csr_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse.csr import csr_matrix
from collections import Counter, defaultdict
import pickle

@numba.jit(forceobj=True)
def get_parents_list(tree_dict: dict, element_id: str, paternts_list: list = None) -> list:
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
        return get_parents_list(tree_dict, element_id=parent_id, paternts_list=paternts_list)



def build_children_features(df: pd.DataFrame):
    from collections import Counter

    logger.info('select all leafs (nodes which are not parents)')
    leafs_set = set(df.element_id.values) - set(df.parent_id.values)
    logger.info(
        f'Leafs set size: {len(leafs_set)} (nodes which have no children)')
    df['is_leaf'] = df.element_id.apply(lambda x: 1 if x in leafs_set else 0)

    logger.info('count number of references to leafs')
    num_leafs_dict = Counter(
        df[df.element_id.isin(leafs_set)].parent_id.values)
    logger.info(
        f'Nodes with leafs as children set size: {len(num_leafs_dict)} (nodes which have leafs as children)')
    df['num_leafs'] = df.element_id.map(num_leafs_dict).fillna(0.0)

    logger.info('count num children for each node')
    num_children_dict = Counter(df.parent_id.values)
    logger.info(f"Nodes with children: {len(num_children_dict)}")
    df['num_children'] = df.element_id.map(num_children_dict).fillna(0.0)

    logger.info('sum of children widths, heights, counts')
    stats_df = df.groupby('parent_id').agg(
        {'width': 'sum', 'height': 'sum', 'parent_id': 'count'})
    stats_df.columns = ['sum_children_widths',
                        'sum_children_heights', 'num_children']
    stats_df.reset_index(inplace=True)

    logger.info('Sum of children widths')
    children_widths_dict = dict(
        stats_df[['parent_id', 'sum_children_widths']].values)
    df['sum_children_widths'] = df.element_id.map(
        children_widths_dict).fillna(0.0)

    logger.info('Sum of children hights')
    children_heights_dict = dict(
        stats_df[['parent_id', 'sum_children_heights']].values)
    df['sum_children_hights'] = df.element_id.map(
        children_heights_dict).fillna(0.0)

    # return  {'leafs':leafs_set, 'num_leafs':num_leafs_dict, 'num_children': num_children_dict } # noqa
    return df



def followers_features(df: pd.DataFrame, followers_set: set = None, level=0) -> pd.DataFrame:
    """
        Build feature: "children_tags" and max reverse depth ( depth from leafs) # noqa
        Concatenate all children tag_names into a string filed 'children_tags'
    """
    # get leafs (nodes without children)
    if followers_set is None:
        level = 0
        followers_set = set(df.element_id.values) - set(df.parent_id.values)
        followers_tags_df = \
            df[df.element_id.isin(followers_set)][['parent_id', 'tag_name']]\
            .groupby('parent_id')['tag_name']\
            .apply(lambda x: ','.join(x))\
            .reset_index()
        followers_tags_dict = dict(followers_tags_df.values)
        df['followers_tags'] = df.element_id.map(
            followers_tags_dict).fillna('')

        # create max_depth field
        df['max_depth'] = 0
        df.max_depth = df.max_depth + \
            df.element_id.isin(set(followers_tags_dict.keys())).astype(int)

        # recursive call
        followers_features(df=df, followers_set=set(
            followers_tags_dict.keys()), level=level + 1)

    elif len(followers_set) > 0:
        # print(f'level: {level}')
        followers_tags_df = \
            df[df.element_id.isin(followers_set)][['parent_id', 'tag_name']]\
            .groupby('parent_id')['tag_name']\
            .apply(lambda x: ','.join(x))\
            .reset_index()
        followers_tags_dict = dict(followers_tags_df.values)
        df['followers_tags'] = df.followers_tags + ',' + \
            df.element_id.map(followers_tags_dict).fillna('')

        # increase max_depth
        df.max_depth = df.max_depth + \
            df.element_id.isin(set(followers_tags_dict.keys())).astype(int)

        # recursive call
        followers_features(df=df, followers_set=set(
            followers_tags_dict.keys()), level=level + 1)

    df['followers_tags'] = df['followers_tags'].apply(
        lambda x: re.sub('\\s+', ' ', x.replace(',', ' ')).lower().strip())
    return df


def build_tree_features(elements_df: pd.DataFrame) -> pd.DataFrame:
    """
        Walk on elements tree and build tree-features:
           - chilren_tags
           - folloer_counters
    """

    def empty_string():
        return ''

    tree_dict = build_tree_dict(elements_df)

    # Build paths
    followers_counter = Counter()
    # level_dict = defaultdict(int)
    children_tags_dict = defaultdict(empty_string)

    with trange(elements_df.shape[0]) as tbar:
        tbar.set_description('Build tree features')
        for i, r in elements_df.iterrows():
            list_of_parents = get_parents_list(
                tree_dict=tree_dict, element_id=r.element_id)
            children_tags_dict[r.parent_id] += r.tag_name.lower() + ' '
            # print(list_of_parents)
            # calculate number of followers
            followers_counter.update(list_of_parents)
            tbar.update(1)

    elements_df['children_tags'] = elements_df.element_id.map(
        children_tags_dict).fillna('')
    elements_df['num_followers'] = elements_df.element_id.map(
        followers_counter)
    return elements_df


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





def get_siblings(siblings_dict: dict, tree_dict: dict, index_dict: dict, element_id: str):
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

def build_children_tags(df: pd.DataFrame, colname='children_tags') -> csr_matrix:
    model_file_path = 'MUI_model/model/tfidf_children_tags.pkl'
    logger.info(f'used column: {colname}')

    if os.path.exists(model_file_path):
        logger.info("TfIdfVectorizer for children tags exists. Loading...")
        with open(model_file_path, 'rb') as f:
            model = pickle.load(file=f)
        child_tags_series = df[colname].fillna('n/a')   


    else:
        logger.info("TfIdfVectorizer for children tags does not exist. Build the one.")
#         if len(set(df.columns).intersection(set(['label', 'label_text']))) != 2:
#             raise Exception('Cannot prepare CountVectorizer for attribute "class": need labels')

        logger.info("Extract useful child_tags features, 'children_tags' column will be used")
        child_tags_series =  df[colname].fillna('')

        child_cv = CountVectorizer()
        child_cv.fit(child_tags_series.values)
        # filter out class names:  length is at least 2 characters and only letters
        vocabulary = sorted([v for v in child_cv.vocabulary_.keys() if re.match(r'^[a-z][a-z]+$', v)])

        logger.info(f'Column ["{colname}"] used for tfidf')
        child_tags_series = df[colname].fillna('')
        model = TfidfVectorizer(vocabulary=vocabulary)  # CountVectorizer?
        model.fit(child_tags_series.values)
        logger.info(f'Saving {model_file_path}, vocabulary length: {len(vocabulary)}')
        with open(model_file_path, 'wb') as f:
            pickle.dump(model, f)
            f.flush()

    return model.transform(child_tags_series.values)


def build_followers_tags(df: pd.DataFrame, colname='followers_tags') -> csr_matrix:
    model_file_path = 'MUI_model/model/tfidf_followers_tags.pkl'
    logger.info(f'used column: {colname}')

    if os.path.exists(model_file_path):
        logger.info("TfIdfVectorizer for children tags exists. Loading...")
        with open(model_file_path, 'rb') as f:
            model = pickle.load(file=f)
        foll_tags_series = df[colname].fillna('n/a')   


    else:
        logger.info("TfIdfVectorizer for followers tags does not exist. Build the one.")
#         if len(set(df.columns).intersection(set(['label', 'label_text']))) != 2:
#             raise Exception('Cannot prepare CountVectorizer for attribute "class": need labels')

        logger.info("Extract useful foll_tags features, 'followers_tags' column will be used")
        foll_tags_series =  df[colname].fillna('')

        foll_cv = CountVectorizer()
        foll_cv.fit(foll_tags_series.values)
        # filter out class names:  length is at least 2 characters and only letters
        vocabulary = sorted([v for v in foll_cv.vocabulary_.keys() if re.match(r'^[a-z][a-z]+$', v)])

        logger.info(f'Column ["{colname}"] used for tfidf')
        foll_tags_series = df[colname].fillna('')
        model = TfidfVectorizer(vocabulary=vocabulary)  # CountVectorizer?
        model.fit(foll_tags_series.values)
        logger.info(f'Saving {model_file_path}, vocabulary length: {len(vocabulary)}')
        with open(model_file_path, 'wb') as f:
            pickle.dump(model, f)
            f.flush()

    return model.transform(foll_tags_series.values)


def build_features(df: pd.DataFrame) -> pd.DataFrame:

    build_is_hidden(df)
    followers_features(df)
    build_children_features(df)
    build_tree_features(df)
    siblings_dict = build_siblings_dict(df)
    index_dict = {idx: r.element_id for idx,
                  r in df.iterrows() if r.element_id != r.parent_id}

    # elements_dict = build_elements_dict(df)
    tree_dict = build_tree_dict(df)

    elements = df.element_id.values  # get siblings for each element

    siblings = [get_siblings(siblings_dict=siblings_dict,
                             tree_dict=tree_dict,
                             index_dict=index_dict,
                             element_id=e)
                for e in elements]

    df['upper_sibling'] = [s[0] for s in siblings]
    df['lower_sibling'] = [s[1] for s in siblings]
    df['siblings'] = siblings

    return df


def attributes_list(file_path='MUI_model/dataset/EXTRACT_ATTRIBUTES_LIST.pkl'):
    with open(file_path, 'rb') as f:
        EXTRACT_ATTRIBUTES_LIST = pickle.load(f)
    return EXTRACT_ATTRIBUTES_LIST


EXTRACT_ATTRIBUTES_LIST = attributes_list()


def build_attributes_feature(df: pd.DataFrame, colname='attributes') -> pd.DataFrame:
    """
        df must have "attributes" field and we are going
        to extract flag whether the attribute exist or not
        colname should be one from the list [
            'attributes', 'attributes_parent', 'attributes_up_sibling', 'attributes_dn_sibling'
            ]
    """
    logger.info(f'used column: {colname}')
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


def build_class_feature(df: pd.DataFrame, colname='attributes') -> csr_matrix:
    """
        Extract TfIdf features for "class" attribute from a column
        containing attributes ("attributes", "attributes_parent", "attributes_up_sibling"...)
        default columns: "attributes"
    """
    model_file_path = 'MUI_model/model/tfidf_attr_class.pkl'
    logger.info(f'used column: {colname}')

    if os.path.exists(model_file_path):
        logger.info("TfIdfVectorizer for class attribute exists. Loaging...")
        with open(model_file_path, 'rb') as f:
            model = pickle.load(file=f)
        attr_class_series = df[colname].apply(lambda x: None if type(x) is not dict else x.get('class')).fillna('')

    else:
        logger.info("TfIdfVectorizer for class attribute does not exist. Build the one.")
#         if len(set(df.columns).intersection(set(['label', 'label_text']))) != 2:
#             raise Exception('Cannot prepare CountVectorizer for attribute "class": need labels')

        logger.info("Extract useful attr_class features, 'attributes' column will be used")
        attr_class_series = df[df.label_text != 'n/a']\
            .attributes.apply(lambda x: None if type(x) is not dict else x.get('class'))\
            .fillna('')

        class_cv = CountVectorizer()
        class_cv.fit(attr_class_series.values)
        # filter out class names:  length is at least 2 characters and only letters
        vocabulary = sorted([v for v in class_cv.vocabulary_.keys() if re.match(r'^[a-z][a-z]+$', v)])

        logger.info(f'Column ["{colname}"] used for tfidf')
        attr_class_series = df[colname].apply(lambda x: None if type(x) is not dict else x.get('class')).fillna('')
        model = TfidfVectorizer(vocabulary=vocabulary)  # CountVectorizer?
        model.fit(attr_class_series.values)
        logger.info(f'Saving {model_file_path}, vocabulary length: {len(vocabulary)}')
        with open(model_file_path, 'wb') as f:
            pickle.dump(model, f)
            f.flush()

    return model.transform(attr_class_series.values)


def build_tag_name_feature(df: pd.DataFrame, colname='tag_name') -> csr_matrix:
    """
        colname should be one of ['tag_name', 'tag_name_parent', 'tag_name_up_sibling', 'tag_name_dn_sibling']
    """
    model_file_path = 'MUI_model/model/ohe_tag_name.pkl'
    logger.info(f'used column: {colname}')

    if os.path.exists(model_file_path):
        logger.info(f'loading {model_file_path}')
        with open(model_file_path, 'rb') as f:
            model = pickle.load(f)
    else:
        logger.info('Building OHE for "tag_name"')
        tag_name_series = df[df.label_text != 'n/a'].tag_name.value_counts()
        tag_name_lst = sorted(list(tag_name_series.index))
        model = OneHotEncoder(handle_unknown='ignore', categories=[tag_name_lst])
        logger.info(f'OHE "tag_name" categories: {model.categories}')
        model.fit(np.expand_dims(df.tag_name.values, -1))
        with open(model_file_path, 'wb') as f:
            logger.info(f'Saving {model_file_path}')
            pickle.dump(model, f)
            f.flush()

    return model.transform(np.expand_dims(df[colname].values, -1))


def build_role_feature(df: pd.DataFrame, colname='attributes') -> csr_matrix:
    model_file_path = 'MUI_model/model/ohe_role.pkl'
    logger.info(f'used column: {colname}')

    if os.path.exists(model_file_path):
        logger.info(f'loading {model_file_path}')
        with open(model_file_path, 'rb') as f:
            ohe = pickle.load(f)
    else:
        logger.info('Building OHE for "role"')
        # We'll use only target's data
        attr_role_series = df[df.label_text != 'n/a'].attributes\
            .apply(lambda x: None if type(x) is not dict else x.get('role'))\
            .fillna('')
        ohe = OneHotEncoder(handle_unknown='ignore').fit(np.expand_dims(attr_role_series.values, -1))
        logger.info(f'OHE "role" categories: {ohe.categories}')
        with open(model_file_path, 'wb') as f:
            logger.info(f'Saving {model_file_path}')
            pickle.dump(ohe, f)
            f.flush()

    attr_role_series = df[colname]\
        .apply(lambda x: None if type(x) is not dict else x.get('role'))\
        .fillna('')

    return ohe.transform(np.expand_dims(attr_role_series, -1))


def build_type_feature(df: pd.DataFrame, colname='attributes') -> csr_matrix:
    model_file_path = 'MUI_model/model/ohe_type.pkl'
    logger.info(f'used column: {colname}')

    if os.path.exists(model_file_path):
        logger.info(f'loading {model_file_path}')
        with open(model_file_path, 'rb') as f:
            ohe = pickle.load(f)
    else:
        logger.info('Building OHE for "type"')
        # We'll use only target's data
        attr_type_series = df[df.label_text != 'n/a'].attributes\
            .apply(lambda x: None if type(x) is not dict else x.get('type'))\
            .fillna('')
        ohe = OneHotEncoder(handle_unknown='ignore').fit(np.expand_dims(attr_type_series.values, -1))
        logger.info(f'OHE "type" categories: {ohe.categories}')
        with open(model_file_path, 'wb') as f:
            logger.info(f'Saving {model_file_path}')
            pickle.dump(ohe, f)
            f.flush()

    attr_type_series = df[colname]\
        .apply(lambda x: None if type(x) is not dict else x.get('type'))\
        .fillna('')

    return ohe.transform(np.expand_dims(attr_type_series, -1))


logger.info('feature_bilder module is loaded...')
