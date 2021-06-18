import os
import re

import numba
import pandas as pd
import numpy as np
import logging
from tqdm.auto import trange
from .dataset_collector import collect_dataset
from .features_builder import build_features

from .common import iou_xywh, build_tree_dict, load_gray_image  # noqa
from .labels import assign_labels


from collections import Counter, defaultdict
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
from glob import glob
from .config import logger
from IPython.display import display  # noqa

FULL_HD_WIDTH = 1920
FULL_HD_HEIGHT = 1080


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


def get_grey_image(file_path: str) -> np.ndarray:
    img = plt.imread(file_path)
    img = (img[..., 0] + img[..., 1] + img[..., 2]) / 3.0
    return img


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


def rebalance(y: np.ndarray):
    logger.info('Rebalance dataset')

    with open('dataset/classes.txt', 'r') as f:
        decoder_dict = {i: v.strip() for i, v in enumerate(f.readlines())}

    proportion_df = pd.DataFrame([
        {'label': i, 'label_text': decoder_dict[i], 'cnt': np.where(y == i)[
            0].shape[0]}
        for i in range(0, len(decoder_dict))
    ])

    labels_cnt = proportion_df[proportion_df.label_text != 'n/a'][['cnt']].sum().values[0]
    na_label_cnt = proportion_df[proportion_df.label_text == 'n/a'].cnt.values[0]
    logger.info(f'"n/a" count: {na_label_cnt}, labels count: {labels_cnt}')

    proportion_df['ratio'] = proportion_df.apply(
        lambda r: na_label_cnt // r.cnt // 7 if (r.label_text != 'n/a') and (r.cnt > 0) else 1, axis=1)

    proportion_df['cnt_rebalanced'] = proportion_df.ratio * proportion_df.cnt
    # display(proportion_df)

    indices = []
    for i, r in proportion_df.iterrows():
        lst = np.where(y == r.label)[0].tolist()
        for _ in range(r.ratio):
            indices.extend(lst)

    np.random.shuffle(indices)
    logger.info(f'Rebalanced and shuffled indices: {len(indices)}')

    return indices


class JDNDataset(Dataset):

    def __init__(self, datasets_list: list = None, rebalance_and_shuffle: bool = False):

        super(JDNDataset, self).__init__()
        self.rebalance_and_suffle = rebalance_and_shuffle

        with open('dataset/classes.txt', 'r') as f:
            lines = f.readlines()
            self.classes_dict = {v.strip(): i for i, v in enumerate(lines)}
            self.classes_reverse_dict = {i: v.strip() for i, v in enumerate(lines)}

        if datasets_list is None:
            logger.info('Will use all available datasets')
            ds_files = glob('dataset/df/*.parquet')
            ds_files = [(fn, 'dataset/annotations/' + re.split(r'[/\\]', re.sub(r'\.parquet$', '', fn))[-1] + '.txt')
                        for fn in ds_files]
        else:
            ds_files = [(f'dataset/df/{fn}.parquet', f'dataset/annotations/{fn}.txt') for fn in datasets_list]

        # display(ds_files)

        df_list = []

        logger.setLevel(logging.ERROR)
        with trange(len(ds_files)) as bar:
            for df_file_path, ann_file_path in ds_files:
                if not os.path.exists(df_file_path):
                    logger.error(f'File: {df_file_path} does not extst')
                else:
                    bar.set_postfix_str(f'{df_file_path}, {ann_file_path}')
                    df = pd.read_parquet(df_file_path)
                    df = build_features(df)
                    df = assign_labels(
                        df=df, annotations_file_path=ann_file_path)
                    df_list.append(df)
                bar.update(1)

        logger.setLevel(logging.DEBUG)

        self.df = pd.concat(df_list)
        logger.info(f'self.df.shape: {self.df.shape}')

        logger.info('Check for duplicates...')
        if self.df.element_id.nunique() != self.df.shape[0]:
            logger.fatal('There are duplicates in the dataset')
            raise Exception('There are duplicates in the dataset')
        logger.info('Check for duplicates is OK')

        self.X, self.y = collect_dataset(self.df)

        if self.rebalance_and_suffle:
            self.indices = np.array(rebalance(self.y))
        else:
            self.indices = np.array([i for i in range(len(self.y))])

    def __getitem__(self, idx):
        return self.X[self.indices[idx]], self.y[self.indices[idx]]

    def __len__(self):
        return self.indices.shape[0]


logger.info("dataset module is loaded...")
