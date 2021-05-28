import numba
import pandas as pd
import numpy as np
import torch

from .common import iou_xywh, build_tree_dict
from .hidden import build_is_hidden
from tqdm.auto import tqdm, trange
import os
import re
import gc

from collections import Counter, defaultdict
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
import glob
from scipy.sparse import vstack, csr_matrix
from .config import logger
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack
import pickle

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


PRIORITY_TAG_SCALERS = {  # We have to scale IoU for certain tags
    'a': 1.,
    'button': 1.,
    'input': 1.,
}


def assign_labels(df: pd.DataFrame, annotations_file_path: str, img: np.ndarray, dummy_value=-1.0) -> pd.DataFrame:
    """
        mark up dataset: assign labels
        annotations_file_path: yolo-v3 formatted annotation

    """

    df['scalar'] = df.tag_name.map(PRIORITY_TAG_SCALERS).fillna(1.0)
    _ann = np.loadtxt(annotations_file_path)
    _boxes = df[['x', 'y', 'width', 'height', 'scalar']].values

    labels = []

    for bb in tqdm(_ann, desc='Assigning labels'):
        c, x, y, w, h = bb
        x = (x - w / 2) * img.shape[1]
        y = (y - h / 2) * img.shape[0]
        w = w * img.shape[1]
        h = h * img.shape[0]

        best_iou = 0.0
        best_i = 0

        for i, r in enumerate(_boxes):  # r[5]: 'is_hidden' - Let's skip hidden nodes

            if (r[2] <= 0) or (r[3] <= 0) or (r[0] < 0) or (r[1] < 0):
                continue

            _iou = iou_xywh((x, y, w, h), (r[0], r[1], r[2], r[3])) * r[4]  # r[4] is a scalar

            if _iou >= best_iou:  # We have to use >=, because the next tag might be more important
                best_i, best_iou = (i, _iou)

        labels.append({'idx': best_i, 'label': c, 'iou': best_iou})

    labels_df = pd.DataFrame(data=labels)
    labels_df.index = labels_df.idx
    df = df.merge(labels_df, how='left', left_index=True, right_index=True)
    df.label = df.label.fillna(dummy_value)
    df.drop(columns=['iou', 'idx'], inplace=True)  # drop auxiliary columns

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
        Walk on elements tree and build tree-features
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


class JDIDataset(Dataset):

    def __init__(self, dataset_names: list = None, rebalance=False):
        super(JDIDataset, self).__init__()
        self.rebalanced = rebalance

        with open('dataset/classes.txt', 'r') as f:
            self.classes_dict = {
                class_name.strip(): i for i, class_name in enumerate(f.readlines())}
            self.classes_reverse_dict = {
                v: k for k, v in self.classes_dict.items()}
        self.dummy_class_value = self.classes_dict['n/a']

        if dataset_names is None:
            logger.warning('Using all available data to generate dataset')
            dataset_names = JDIDataset.gen_dataset_names()

        logger.info(f"List of dataset_names:{dataset_names}")

        ds_list = []  # list of datasets to join

        # Read and concatenate all listed datasets
        for ds_name in dataset_names:
            logger.info(f'Dataset for {ds_name}')
            df = pd.read_parquet(f'dataset/df/{ds_name}.parquet')
            logger.info(f"Dataset shape: {df.shape}")

            logger.info('cleaning tag_name from dummy/auxiliary words')
            df.tag_name = df.tag_name.apply(
                lambda x: x.lower().replace('-example', ''))  # tag_name LOWER()
            df = build_is_hidden(df=df)
            df = build_children_features(df=df)
            df = build_tree_features(df)
            df = followers_features(df)
            # df.width = (FULL_HD_WIDTH - df.width) / FULL_HD_WIDTH
            # df.height = (FULL_HD_HEIGHT - df.height) / FULL_HD_HEIGHT

            # ----------------------------------------------------------------------------------------------
            # Merge children with parents
            # WARNING: There is a tag <HTML> without parent. Let's fix this issue
            df.parent_id = df.apply(
                lambda r: r.element_id if r.parent_id is None else r.parent_id, axis=1)
            df = df.merge(df, left_on='parent_id',
                          right_on='element_id', suffixes=('', '_parent'))
            logger.info(
                f"Dataset shape after merging with parents: {df.shape}")
            # ----------------------------------------------------------------------------------------------

            # If annotation file exists, lets load it and assign labels
            if os.path.exists(f'dataset/annotations/{ds_name}.txt'):
                logger.warning(
                    f'Load LABELS from dataset/annotations/{ds_name}.txt')
                img = plt.imread(f'dataset/images/{ds_name}.png')
                df = assign_labels(df, annotations_file_path=f'dataset/annotations/{ds_name}.txt',
                                   img=img,
                                   dummy_value=self.dummy_class_value
                                   )
                del img
            else:
                logger.warning(
                    'assign dummy values [n/a] for labels if there is no annotations')
                df['label'] = self.dummy_class_value

            df['ds_name'] = ds_name
            ds_list.append(df)
            gc.collect()

        logger.info('Concatenate datasets')
        self.dataset = pd.concat(ds_list)
        logger.info(f"Dataset shape after reading: {self.dataset.shape}")

        if rebalance:
            self._oversample()

        self._count_vectorizer_class()

        # add ohe_ columns to one hot encoding several attributes
        for attr in ['role', 'type', 'ui']:
            logger.info(f'Build OHE column for attribute {attr}')
            self.dataset['ohe_' + attr] = self.dataset['attributes'].apply(
                lambda x: x.get(attr)).fillna("").str.lower()

        for attr in ['role', 'type', 'ui']:
            logger.info(f'Build OHE column for attribute {attr}_parent')
            self.dataset['ohe_' + attr + '_parent'] = self.dataset['attributes_parent'].apply(
                lambda x: x.get(attr)).fillna("").str.lower()

        logger.info('OHE tag_name')
        self.tag_name_sm = self._ohe_column('tag_name')
        logger.info(f'tag_name_sm.shape: {self.tag_name_sm.shape}')

        logger.info('OHE tag_name_parent')
        self.tag_name_parent_sm = self._ohe_column(
            colname='tag_name_parent', ohe_file_path='model/tag_name.pkl')
        logger.info(
            f'tag_name_parent_sm.shape: {self.tag_name_parent_sm.shape}')

        logger.info('OHE ohe_role')
        self.ohe_role_sm = self._ohe_column('ohe_role')
        logger.info(f'ohe_role_sm.shape: {self.ohe_role_sm.shape}')

        logger.info('OHE ohe_role_parent')
        self.ohe_role_parent_sm = self._ohe_column(
            colname='ohe_role_parent', ohe_file_path='model/ohe_role.pkl')
        logger.info(
            f'ohe_role_parent_sm.shape: {self.ohe_role_parent_sm.shape}')

        logger.info('OHE ohe_type')
        self.ohe_type_sm = self._ohe_column('ohe_type')
        logger.info(f'ohe_type_sm.shape: {self.ohe_type_sm.shape}')

        logger.info('OHE ohe_type_parent')
        self.ohe_type_parent_sm = self._ohe_column(
            colname='ohe_type_parent', ohe_file_path='model/ohe_type.pkl')
        logger.info(
            f'ohe_type_parent_sm.shape: {self.ohe_type_parent_sm.shape}')

        logger.info('OHE ohe_ui')
        self.ohe_ui_sm = self._ohe_column('ohe_ui')
        logger.info(f'ohe_ui_sm.shape: {self.ohe_ui_sm.shape}')

        logger.info('OHE ohe_ui_parent')
        self.ohe_ui_parent_sm = self._ohe_column(
            'ohe_ui_parent', ohe_file_path='model/ohe_ui.pkl')
        logger.info(f'ohe_ui_parent_sm.shape: {self.ohe_ui_parent_sm.shape}')

        # extract all non null attributes names
        self.dataset['attributes_text'] = self.dataset.attributes.apply(
            lambda x: " ".join([k for k in x.keys() if x[k] is not None]))
        logger.info('Fit CountVectorizer for column "attributes"')
        self.attributes_sm = self._count_vectorizer_column('attributes_text')
        logger.info(f'attributes_sm.shape: {self.attributes_sm.shape}')

        # children_tags
        file_path = 'model/count_vectorizer_children_tags.pkl'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                logger.warning(
                    f'Load CountVectorizer for column "chidren_tags": {file_path}')
                self.count_vectorizer_chilgren_tags = pickle.load(f)
        else:
            logger.warning(
                f'Saving CountVectorizer for "children_tags": {file_path}')
            self.count_vectorizer_chilgren_tags = CountVectorizer().fit(
                self.dataset.children_tags.values)
            with open(file_path, 'wb') as f:
                pickle.dump(self.count_vectorizer_chilgren_tags, f)
        logger.info(
            f'CountVectorizer "chilren_tags" size: {len(self.count_vectorizer_chilgren_tags.vocabulary_)}')
        self.children_tags_sm = self.count_vectorizer_chilgren_tags.transform(
            self.dataset.children_tags.values)
        logger.info(f"chidren_tags_sm: {self.children_tags_sm.shape}")

        # followers_tags
        file_path = 'model/count_vectorizer_followers_tags.pkl'
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                logger.warning(
                    f'Load CountVectorizer for column "followers_tags": {file_path}')
                self.count_vectorizer_followers_tags = pickle.load(f)
        else:
            logger.warning(
                f'Saving CountVectorizer for "followers_tags": {file_path}')
            self.count_vectorizer_followers_tags = CountVectorizer().fit(
                self.dataset.followers_tags.values)
            with open(file_path, 'wb') as f:
                pickle.dump(self.count_vectorizer_followers_tags, f)
        logger.info(
            f'CountVectorizer "followers_tags" size: {len(self.count_vectorizer_followers_tags.vocabulary_)}')
        self.followers_tags_sm = self.count_vectorizer_followers_tags.transform(
            self.dataset.followers_tags.values)
        logger.info(f"followers_tags_sm: {self.followers_tags_sm.shape}")

        # self.followers_tags_parent_sm = self.count_vectorizer_followers_tags.transform(  # PARENT's followers tags, acc = 0.8720 # noqa
        #     self.dataset.followers_tags_parent.values)
        # logger.info(f"followers_tags_parent_sm: {self.followers_tags_parent_sm.shape}")

        # extract all non null attributes names
        self.dataset['attributes_parent_text'] = self.dataset.attributes_parent.apply(
            lambda x: " ".join([k for k in x.keys() if x[k] is not None]))
        logger.info('Fit CountVectorizer for column "attributes_parent"')
        self.attributes_parent_sm = \
            self._count_vectorizer_column(colname='attributes_parent_text',
                                          file_path='model/count_vectorizer_attributes_text.pkl')
        logger.info(
            f'attributes_parent_sm.shape: {self.attributes_parent_sm.shape}')

        self._extract_features()

        self.labels = self.dataset.label.astype(
            int).map(self.classes_reverse_dict)
        self.dataset.label = self.dataset.label.astype(int)

        self.data = hstack([
            self.attributes_sm,
            self.tag_name_sm,
            self.ohe_role_sm,
            self.ohe_type_sm,
            self.ohe_ui_sm,
            self.tag_name_parent_sm,
            self.ohe_type_parent_sm,
            self.ohe_role_parent_sm,
            self.ohe_ui_parent_sm,
            self.attributes_parent_sm,
            self.features_df.values,
            self.children_tags_sm,
            self.followers_tags_sm,
            # self.followers_tags_parent_sm,
            self.class_sm
        ]).astype(np.float32)

        self.data = csr_matrix(self.data)

        logger.info(f'OHE columns sparse matrix: {self.data.shape}')

    def __len__(self):
        return self.data.shape[0]

    def __getitem__(self, idx):
        # return np.array(self.data.getrow(idx).todense()[0]).squeeze(), self.dataset.iloc[idx]['label']
        return idx

    def collate_fn(self, batch):
        return torch.tensor(vstack([self.data.getrow(idx) for idx in batch]).todense().astype(np.float32)), \
            torch.tensor(self.dataset.iloc[batch]
                         ['label'].values.astype(np.int64))

    def _oversample(self):
        logger.warning(
            'Oversample data to balance the dataset, this will create duplicated rows in dataset')

        class_counts = [r for r in self.dataset.label.value_counts(
        ).sort_values(ascending=False).items()]
        max_count = class_counts[0][1]

        dfs = [self.dataset]
        for cc in class_counts[1:]:
            ratio = max_count // cc[1]
            ratio = 30 if ratio >= 30 else ratio
            for _ in range(ratio):
                dfs.append(self.dataset[self.dataset.label == cc[0]].copy())

        self.dataset = pd.concat(dfs)
        logger.warning(f'Rebalanced dataset size: {self.dataset.shape[0]}')

    def _ohe_column(self, colname, ohe_file_path=None):
        """
            load attr_ohe if exists model/attr_ohe.pkl
            otherwise build the one
        """
        if ohe_file_path is None:
            file_path = f'model/{colname}.pkl'
        else:
            file_path = ohe_file_path

        if os.path.exists(file_path):
            logger.warning(
                f'loading existing OHE for column "{colname}" from {file_path}')
            with open(file_path, 'rb') as f:
                ohe = pickle.load(f)
        else:
            logger.warning(f'Create and fit OHE for column "{colname}"')
            ohe = OneHotEncoder(handle_unknown='ignore')
            ohe.fit(np.expand_dims(self.dataset[colname].values, axis=1))
            with open(file_path, 'wb') as f:
                pickle.dump(ohe, f)

        sm = ohe.transform(np.expand_dims(
            self.dataset[colname].values, axis=1))
        return sm

    def _count_vectorizer_column(self, colname, file_path=None):
        """
            load count_vercorizer for a column if a pkl file exists
            otherwise create the one
        """
        if file_path is None:
            file_path = f'model/count_vectorizer_{colname}.pkl'

        if os.path.exists(file_path):
            logger.warning(
                f'loading existing count vectorizer for column "{colname}" from {file_path}')
            with open(file_path, 'rb') as f:
                vectorizer = pickle.load(f)
            self.vocabulary = vectorizer.vocabulary_
        else:
            logger.warning(
                f'Create and fit count vectorizer for column "{colname}"')
            vectorizer = CountVectorizer(vocabulary=self._build_vocabulary())
            vectorizer.fit(self.dataset[colname].values)
            with open(file_path, 'wb') as f:
                pickle.dump(vectorizer, f)

        sm = vectorizer.transform(self.dataset[colname].values)
        return sm

    def _build_vocabulary(self):
        """
            Attempt to reduce number of features by removing rarely used attributes

        """

        attributes_usage = Counter()
        for attr_list in self.dataset.attributes.apply(lambda x: [field for field in x if x[field] is not None]).values:
            attributes_usage.update(attr_list)

        attributes_usasge_df = pd.DataFrame(
            [[attribute, cnt] for attribute, cnt in attributes_usage.items()],
            columns=['attribute', 'cnt']
        ).sort_values(by='cnt', ascending=False)

        # Lets cut off attributes which are rarely used
        attributes_list_df = attributes_usasge_df[attributes_usasge_df.cnt > 1].copy()

        attr_unique_values_map = {
            attr: self.dataset['attributes'].apply(
                lambda x: x.get(attr)).nunique()
            for attr in (attributes_list_df.attribute.values)
        }
        attributes_list_df['num_unique_values'] = attributes_list_df.attribute.map(
            attr_unique_values_map)
        attributes_list_df['k'] = attributes_list_df.cnt / attributes_list_df.num_unique_values

        attributes_list_df = attributes_list_df[
            (attributes_list_df.k > 3.0) & (attributes_list_df.num_unique_values > 1)
        ].sort_values(by='cnt', ascending=False).copy()

        self.vocabulary = {w: i for i, w in enumerate(
            sorted(attributes_list_df.attribute.values))}
        return self.vocabulary

    def _extract_features(self):
        self.features_df = self.dataset[[
            # 'tag_name_parent',
            # 'tag_name',
            'width',
            'height',
            'width_parent',
            'height_parent',
            # 'x',
            # 'x_parent',
            # 'y',
            # 'y_parent',
            'is_leaf',
            'is_leaf_parent',
            'num_followers',
            'num_leafs',
            'num_leafs_parent',
            'max_depth',
            'num_children',
            'num_children_parent',
            'sum_children_widths',
            'sum_children_widths_parent',
            'sum_children_hights',
            'sum_children_hights_parent',
            'displayed',
            'is_hidden',
            # 'onmouseenter'
        ]].copy()

        self.features_df.sum_children_hights = (
            self.features_df.sum_children_hights / self.features_df.num_children).fillna(-1)
        self.features_df.sum_children_hights_parent = (
            self.features_df.sum_children_hights_parent / self.features_df.num_children_parent).fillna(-1)
        self.features_df.sum_children_widths = (
            self.features_df.sum_children_widths / self.features_df.num_children).fillna(-1)
        self.features_df.sum_children_widths_parent = (
            self.features_df.sum_children_widths_parent / self.features_df.num_children_parent).fillna(-1)

        # self.features_df.x = (self.features_df.x < 0).astype(int)
        # self.features_df.y = (self.features_df.y < 0).astype(int)
        # self.features_df.x_parent = (self.features_df.x_parent < 0).astype(int)
        # self.features_df.y_parent = (self.features_df.y_parent < 0).astype(int)
        self.features_df['w'] = (self.features_df.width <= 2).astype(int)
        self.features_df['w_parent'] = (
            self.features_df.width_parent <= 2).astype(int)
        self.features_df['h'] = (self.features_df.height <= 2).astype(int)
        self.features_df['h_parent'] = (
            self.features_df.height_parent <= 2).astype(int)
        self.features_df.displayed = self.features_df.displayed.astype(int)

    @staticmethod
    def find_file_names(self, path_mask='dataset/df/*.parquet'):
        return set([re.sub('.*[/\\\\]', '', re.sub('\\..*$', '', os.path.normpath(fn)))
                    for fn in glob.glob(path_mask)])

    @staticmethod
    def gen_dataset_names():
        dfs = JDIDataset.find_file_names('dataset/df/*.parquet')
        imgs = JDIDataset.find_file_names('dataset/images/*.png')
        anns = JDIDataset.find_file_names('dataset/annotations/*.txt')

        return (dfs.intersection(imgs)).intersection(anns)

    def _count_vectorizer_class(self):
        self.dataset['cv_class'] = self.dataset.attributes.apply(
            lambda x: x.get('class')).fillna('')
        file_name = 'model/count_vectorizer_class.pkl'
        if os.path.exists(file_name):
            logger.warning(
                f'Loading count vectorizer for column "cv_class": {file_name}')
            with open(file_name, 'rb') as f:
                self.count_vectorizer_class = pickle.load(f)
        else:
            logger.warning(
                f'Build count vectorizer for column "cv_class": {file_name}')
            class_dict = Counter()
            for s in self.dataset['cv_class'].values:
                class_dict.update(s.lower().replace('-', ' ').split())
            vocabulary = [
                cls for cls in class_dict if re.match('^[a-z]*$', cls)]
            self.count_vectorizer_class = CountVectorizer(
                vocabulary=vocabulary).fit(self.dataset['cv_class'].values)
            with open(file_name, 'wb') as f:
                pickle.dump(self.count_vectorizer_class, f)
        self.class_sm = self.count_vectorizer_class.transform(
            self.dataset['cv_class'].values)
        logger.info(f'class_sm: {self.class_sm.shape}')


logger.info("dataset module is loaded...")
