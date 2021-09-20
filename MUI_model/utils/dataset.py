import os
import re

import numba
import pandas as pd
import numpy as np
import logging
from tqdm.auto import trange
from MUI_model.utils.dataset_collector import collect_dataset
from MUI_model.utils.features_builder import build_features
from MUI_model.utils.common import build_tree_dict

from MUI_model.utils.common import iou_xywh # noqa
from MUI_model.utils.labels import assign_labels


from collections import Counter, defaultdict
from torch.utils.data import Dataset
import matplotlib.pyplot as plt
from glob import glob
from MUI_model.utils.config import logger
from IPython.display import display  # noqa

def rebalance(y: np.ndarray):
    logger.info('Rebalance dataset')

    with open('MUI_model/dataset/classes.txt', 'r') as f:
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
        lambda r: na_label_cnt // r.cnt // 15 if (r.label_text != 'n/a') and (r.cnt > 0) else 1, axis=1)

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

        with open('MUI_model/dataset/classes.txt', 'r') as f:
            lines = f.readlines()
            self.classes_dict = {v.strip(): i for i, v in enumerate(lines)}
            self.classes_reverse_dict = {i: v.strip() for i, v in enumerate(lines)}

        if datasets_list is None:
            logger.info('Will use all available datasets')
            ds_files = glob('MUI_model/dataset/df/*.pkl')
#             ds_files = [(fn, 'dataset/annotations/' + re.split(r'[/\\]', re.sub(r'\.parquet$', '', fn))[-1] + '.txt')
#                         for fn in ds_files]
        else:
            ds_files = [(f'MUI_model/dataset/df/{fn}.pkl') for fn in datasets_list]
             

        # display(ds_files)

        df_list = []

        logger.setLevel(logging.ERROR)
        with trange(len(ds_files)) as bar:
            for df_file_path in ds_files:
                if not os.path.exists(df_file_path):
                    logger.error(f'File: {df_file_path} does not extst')
                else:
                    bar.set_postfix_str(f'{df_file_path}')
#                     df = pd.read_parquet(df_file_path)
                    df = pd.read_pickle(df_file_path)
                    df['label_text'] = df.attributes.apply(lambda x: x.get('data-label') if x is not None else 'n/a').fillna('n/a')
                    df = build_features(df)
                    df = assign_labels(
                        df=df)
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