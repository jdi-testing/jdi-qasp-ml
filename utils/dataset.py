import numba
import pandas as pd
import numpy as np
import selenium
from selenium.webdriver.chrome.options import Options
from .common import iou_xywh
from tqdm.auto import tqdm, trange
import os, sys, re, gc
import logging
from time import sleep
from collections import Counter
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import glob

from .common import TQDM_BAR_FORMAT, get_all_elements, maximize_window, screenshot, build_elements_dataset
from .config import logger
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import OneHotEncoder
from scipy.sparse import hstack
import pickle

logger.info("dataset package is loaded...")

def build_tree_dict(df:pd.DataFrame) -> dict:
    """
        Builds tree dict for
        get_parents_list 
    """
    tree_dict = dict(zip(df.element_id.values, df.parent_id.values))
    return tree_dict


@numba.jit(forceobj=True)
def get_parents_list(tree_dict:dict, element_id:str, paternts_list:list=[]) -> list:
    """
        returns ordered list of parent for a element
        starting from root which is the <html/> tag
    """
    parent_id = tree_dict.get(element_id)
    if parent_id is None:
        return paternts_list
    else:
        paternts_list.append(parent_id)
        return get_parents_list(tree_dict, element_id=parent_id, paternts_list=paternts_list)


def build_children_features(df:pd.DataFrame):
    from collections import Counter
    
    logger.info('select all leafs (nodes which are not parents)')
    leafs_set = set(df.element_id.values) - set(df.parent_id.values)
    logger.info(f'Leafs set size: {len(leafs_set)} (nodes which have no children)')
    df['is_leaf'] = df.element_id.apply(lambda x: 1 if x in leafs_set else 0)
    
    logger.info('count number of references to leafs')
    num_leafs_dict = Counter(df[df.element_id.isin(leafs_set)].parent_id.values)
    logger.info(f'Nodes with leafs as children set size: {len(num_leafs_dict)} (nodes which have leafs as children)')
    df['num_leafs'] = df.element_id.map(num_leafs_dict).fillna(0.0)

    logger.info('count num children for each node')
    num_children_dict = Counter(df.parent_id.values)
    logger.info(f"Nodes with children: {len(num_children_dict)}")
    df['num_children'] = df.element_id.map(num_children_dict).fillna(0.0)

    logger.info('sum of children widths, heights, counts')
    stats_df = df.groupby('parent_id').agg({'width': 'sum', 'height': 'sum', 'parent_id': 'count'})
    stats_df.columns = ['sum_children_widths', 'sum_children_heights', 'num_children']
    stats_df.reset_index(inplace=True)

    logger.info('Sum of children widths')
    children_widths_dict = dict(stats_df[['parent_id', 'sum_children_widths']].values)
    df['sum_children_widths'] = df.element_id.map(children_widths_dict).fillna(0.0)

    logger.info('Sum of children hights')
    children_heights_dict = dict(stats_df[['parent_id', 'sum_children_heights']].values)
    df['sum_children_hights'] = df.element_id.map(children_heights_dict).fillna(0.0)
    
    #return  {'leafs':leafs_set, 'num_leafs':num_leafs_dict, 'num_children': num_children_dict }
    return df

def get_grey_image(file_path:str) -> np.ndarray:
    img = plt.imread(file_path)
    img = (img[...,0] + img[...,1] + img[...,2])/3.0
    return img


def assign_labels(df:pd.DataFrame, annotations_file_path:str, img:np.ndarray) -> pd.DataFrame:

    """
        mark up dataset: assign labels
        annotations_file_path: yolo-v3 formatted annotation
    """

    _ann = np.loadtxt(annotations_file_path)
    _boxes = df[['x', 'y', 'width', 'height' ]].values

    labels = []

    for bb in tqdm(_ann, desc='Assigning labels'):
        c,x,y,w,h = bb
        x = (x - w/2) * img.shape[1]
        y = (y - h/2) * img.shape[0]
        w = w * img.shape[1]
        h = h * img.shape[0]

        best_iou = 0.0
        best_i = 0
        
        for i, r in enumerate(_boxes):
            
            if (r[2] <= 0) or (r[3] <= 0) or (r[0]<0) or (r[1] < 0) :
                continue
                
            _iou = iou_xywh((x,y,w,h), (r[0], r[1], r[2], r[3]))
            
            if _iou > best_iou:
                best_i, best_iou = (i, _iou)
        
        labels.append({'idx': best_i, 'label': c, 'iou': best_iou })

    labels_df = pd.DataFrame(data=labels)
    labels_df.index = labels_df.idx
    df = df.merge(labels_df, how='left', left_index=True, right_index=True)
    df.label = df.label.fillna(-1.0)
    df.drop(columns=['iou', 'idx'], inplace=True) # drop auxiliary columns

    return df


def build_path_features(elements_df:pd.DataFrame) -> pd.DataFrame:

    """
        Main purpose of this brocedure is an ability to calculate 
        number of followers for a node
    """

    tree_dict = build_tree_dict(elements_df)
    tag_name_dict = dict(zip(elements_df.element_id.values, elements_df.tag_name.values))
    width_dict = dict(zip(elements_df.element_id.values, elements_df.width.values))
    height_dict = dict(zip(elements_df.element_id.values, elements_df.height.values))

    # Build paths
    paths = []
    followers_counter = Counter()

    with trange(elements_df.shape[0]) as tbar:
        tbar.set_description('Generating paths')
        for i, r in elements_df.iterrows():
            list_of_parents = []
            path = []
            get_parents_list(tree_dict=tree_dict, element_id= r.element_id, paternts_list=list_of_parents)
            followers_counter.update(list_of_parents)
            path = "/".join([ tag_name_dict[i]+':'+str(int(width_dict[i])) +':'+str(int(height_dict[i])) 
                                    for i in get_parents_list(tree_dict=tree_dict, element_id=r.element_id, paternts_list=path)])
            paths.append(path)
            tbar.update(1)
    
    elements_df['path'] = paths
    elements_df['num_followers'] = elements_df.element_id.map(followers_counter)
    return elements_df


class DatasetBuilder:
    """
        Build dataset from a specific url
    """

    headless = True

    def __init__(self, url:str, dataset_name:str = 'dummy', headless=True):

        if dataset_name == 'dummy':
            logger.warn('The default dataset name "dummy" will be used')
        else:
            logger.info(f'Dataset name: {dataset_name}')

        super(DatasetBuilder).__init__()
        self.url = url
        self.driver = None
        self.logger = logger
        self.dataset_name = dataset_name
        self.headless = headless
        
        logger.info('Create directories to save the dataset')
        #logger.info('dataset/images')
        os.makedirs('dataset/images', exist_ok=True)
        #logger.info('dataset/df')
        os.makedirs('dataset/df', exist_ok=True)
        #logger.info('dataset/annotations')
        os.makedirs('dataset/annotations', exist_ok=True)
        #logger.info('dataset/html')
        os.makedirs('dataset/html', exist_ok=True)


        self.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('Close web driver')
        self.driver.close()

    def __enter__(self):

        from selenium.webdriver.chrome.options import Options

        if self.driver is not None:
            return self

        self.options = Options()
        self.options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        self.options.add_argument('--skip-js-errors')
        # self.options.add_argument("--start-maximized")
        if self.headless:
            self.options.add_argument('--headless')

        logger.info('Creating driver')
        chrome_driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
        if os.path.exists(chrome_driver_path):
            self.driver = selenium.webdriver.Chrome(executable_path=chrome_driver_path, options=self.options)
        else:
            raise FileNotFoundError(f"chromedriver.exe  {os.getcwd()}")

        logger.info('Chrome web driver is created')
        self.setUp(self.driver)
        self.build_dataset()
        self.build_features()

        return self
       

    def setUp(self, driver):
        """
            This method may be overwitten if you need to login to the site
            and navigate to a specific url,
            otherwise it just returns 
        """
        logger.info(f'getting url: {self.url}')
        self.driver.get(self.url)
        sleep(3.0)
        maximize_window(driver=self.driver)
        sleep(9.0)

    def build_dataset(self):

        #elements_df = get_all_elements(driver=self.driver)
        # At first we have to save screenshot
        logger.info(f'Save color screenshot to dataset/images/{self.dataset_name}.png')
        screenshot(self.driver, save_to_file=f'dataset/images/{self.dataset_name}.png')

        # And HTML sorce
        logger.info(f'Save html to dataset/html/{self.dataset_name}.html')
        with open(f'dataset/html/{self.dataset_name}.html', 'wb') as f:
            f.write(self.driver.page_source.encode())
            f.flush()
 
        # build_elements_dataset calls hover, which changes screenshot, sor it have to be called the very end
        elements_df = build_elements_dataset(driver=self.driver)
        build_path_features(elements_df=elements_df)

        logger.info(f'Save parquet to dataset/df/{self.dataset_name}.parquet')
        elements_df.to_parquet(f'dataset/df/{self.dataset_name}.parquet')

        self.dataset = elements_df
        return self.dataset


    def build_features(self):
        self.dataset = build_children_features(df=self.dataset)

COLUMNS_TO_DROP = {
    'parent_id',
    'parent_id_parent',
    'element_id', 
    'base64png_before_hover', 
    'base64png_after_hover', 
    'base64png_before_hover_parent',
    'base64png_after_hover_parent',
    'x', 'y', 'x_parent', 'y_parent',
    'element_id_parent',
    'path', 
    'path_parent',
    'is_leaf_parent',
    'label_parent',
    'ds_name',
    'hover_before',
    'hover_after',
    'hover_before_parent',
    'hover_after_parent',
    'attr_class',
    'attr_class_parent',
}

class JDIDataset(Dataset):

    def __init__(self, dataset_names:list=None, rebalance=True):
        super(JDIDataset, self).__init__()

        ds_list=[]

        if dataset_names is None:
            logger.warn('Using all availabel data to generate dataset')
            dataset_names = self._gen_dataset_names()

        for ds_name in dataset_names:
            logger.info(f'Dataset for {ds_name}')
            df = pd.read_parquet(f'dataset/df/{ds_name}.parquet')
            logger.info(f"Dataset shape: {df.shape}")

            logger.info('cleaning tag_name from dummy words')
            df.tag_name = df.tag_name.apply(lambda x: x.replace('-example', ''))

            # If exists file with labels, load it
            if os.path.exists(f'dataset/annotations/{ds_name}.txt'):
                logger.warning(f'Load LABELS from dataset/annotations/{ds_name}.txt')
                df = assign_labels(df, annotations_file_path=f'dataset/annotations/{ds_name}.txt', 
                                       img=plt.imread(f'dataset/images/{ds_name}.png'))
            else:
                logger.warning(f'LABELS: not loaded')
                df['label'] = -1.0

            df = build_children_features(df=df)

            # WARNING: There is a tag <HTML> without parent. Let's fix this issue
            df.parent_id = df.apply(lambda r: r.element_id if r.parent_id is None else r.parent_id, axis=1)

            df = df.merge(df, left_on='parent_id', right_on='element_id', suffixes=('', '_parent'))
            logger.info(f"Dataset shape after merging with parents: {df.shape}")

            df['ds_name'] = ds_name
            ds_list.append(df)

        logger.info('Concatenate datasets')
        self.dataset = pd.concat(ds_list)
        logger.info(f"Dataset shape after reading: {self.dataset.shape}")
        
        self.dataset.displayed = self.dataset.displayed.astype(int).fillna(0)
        self.dataset.enabled = self.dataset.enabled.astype(int).fillna(0)
        self.dataset.selected = self.dataset.selected.astype(int).fillna(0)
        self.dataset.text = self.dataset.text.apply(lambda x: 0 if (x is None) else 1)
        self.dataset.attr_id = self.dataset.attr_id.apply(lambda x: 0 if (x is None) else 1)
        self.dataset.hover = self.dataset.hover.fillna(False).astype(int)
        self.dataset.attr_onmouseover = self.dataset.attr_onmouseover.apply(lambda x: 1 if x is not None else 0)
        self.dataset.attr_onclick = self.dataset.attr_onclick.apply(lambda x: 1 if x is not None else 0)
        self.dataset.attr_ondblclick = self.dataset.attr_ondblclick.apply(lambda x: 1 if x is not None else 0)

        self.dataset.displayed_parent = self.dataset.displayed_parent.fillna(0).astype(int)
        self.dataset.enabled_parent = self.dataset.enabled_parent.fillna(0).astype(int)
        self.dataset.selected_parent = self.dataset.selected_parent.fillna(0).astype(int)
        self.dataset.text_parent = self.dataset.text_parent.apply(lambda x: 0 if (x is None) else 1)
        self.dataset.attr_id_parent = self.dataset.attr_id_parent.apply(lambda x: 0 if (x is None) else 1)
        self.dataset.hover_parent = self.dataset.hover_parent.fillna(.0).astype(int)
        self.dataset.attr_onmouseover_parent = self.dataset.attr_onmouseover_parent.apply(lambda x: 1 if x is not None else 0)
        self.dataset.attr_onclick_parent = self.dataset.attr_onclick_parent.apply(lambda x: 1 if x is not None else 0)
        self.dataset.attr_ondblclick_parent = self.dataset.attr_ondblclick_parent.apply(lambda x: 1 if x is not None else 0)
        self.dataset.tag_name_parent = self.dataset.tag_name_parent.fillna('html')

        with open('dataset/classes.txt', 'r') as f:
            classes_list = [c.strip() for c in f.readlines()]

        if rebalance:
            self.rebalance()

        self.dataset['label_text'] = self.dataset.label.apply(lambda x: classes_list[int(x)] if x >=0 else 'n/a')
        self.dataset_copy_df = self.dataset.copy()

        logger.info(f'Drop redundunt columns: {COLUMNS_TO_DROP}')
        self.dataset.drop(columns= set(self.dataset).intersection(COLUMNS_TO_DROP), inplace=True)

        TAG_NAME_COUNT_VECTORIZER = 'model/tag_name_count_vectorizer.pkl'
        if os.path.exists(TAG_NAME_COUNT_VECTORIZER):
            logger.warn('Load existing count vectorizer for tag_names')
            with open(TAG_NAME_COUNT_VECTORIZER,'rb') as f:
                self.tag_name_count_vectorizer = pickle.load(f)
        else:
            logger.info('Create, fit, save CountVectorizer for tag_name')
            self.tag_name_count_vectorizer = CountVectorizer()
            self.tag_name_count_vectorizer.fit(self.dataset.tag_name)
            with open(TAG_NAME_COUNT_VECTORIZER, 'wb') as f:
                pickle.dump(self.tag_name_count_vectorizer, f)

        self.tag_name_sm = self.tag_name_count_vectorizer.transform(self.dataset.tag_name)
        self.tag_name_parent_sm = self.tag_name_count_vectorizer.transform(self.dataset.tag_name_parent)

        # If don't have OHE for attr_type, create, fit and save the one
        ATTR_TYPE_OHE = 'model/attr_type_ohe.pkl'
        if os.path.exists(ATTR_TYPE_OHE):
            logger.warning(f'Load existing attr_type OHE. You have to remove {ATTR_TYPE_OHE}, to fit it from scratch')
            with open(ATTR_TYPE_OHE, 'rb') as f: 
                self.attr_type_ohe = pickle.load(f)
        else:
            logger.warning('Create and fit OHE for attr_type, attr_type_patent')
            self.attr_type_ohe = OneHotEncoder(handle_unknown='ignore')
            self.attr_type_ohe.fit(np.expand_dims(self.dataset.attr_type.values, axis=1))
            with open(ATTR_TYPE_OHE, 'wb') as f:
                pickle.dump(self.attr_type_ohe, f)

        self.attr_type_sm = self.attr_type_ohe.transform(np.expand_dims(self.dataset.attr_type.values, axis=1))
        self.attr_type_parent_sm = self.attr_type_ohe.transform(np.expand_dims(self.dataset.attr_type_parent.values, axis=1))
        
        # if don't have OHE for attr_role, create, fit and save it
        ATTR_ROLE_OHE = 'model/attr_role_ohe.pkl'
        if os.path.exists(ATTR_ROLE_OHE):
            logger.warning(f'Load existing attr_role OHE. You have to remove {ATTR_ROLE_OHE}, to fit it from scratch')
            with open(ATTR_ROLE_OHE, 'rb') as f: 
                self.attr_role_ohe = pickle.load(f)
        else:
            logger.warning('Create and fit OHE for attr_role, attr_role_patent')
            self.attr_role_ohe = OneHotEncoder(handle_unknown='ignore')
            self.attr_role_ohe.fit(np.expand_dims(self.dataset.attr_role.values, axis=1))
            with open(ATTR_ROLE_OHE, 'wb') as f:
                pickle.dump(self.attr_role_ohe, f)

        self.attr_role_sm = self.attr_role_ohe.transform(np.expand_dims(self.dataset.attr_role.values, axis=1))
        self.attr_role_parent_sm = self.attr_role_ohe.transform(np.expand_dims(self.dataset.attr_role_parent.values, axis=1))

        self.sm = hstack([self.attr_role_parent_sm, 
                          self.attr_role_sm, 
                          self.attr_type_parent_sm, 
                          self.attr_type_sm, 
                          self.tag_name_parent_sm, 
                          self.tag_name_sm
                         ]).astype(np.float32)

        LABEL_OHE = 'model/label_ohe.pkl'
        if os.path.exists(LABEL_OHE):
            logger.warning(f'Load existing label OHE from {LABEL_OHE}')
            with open(LABEL_OHE, 'rb') as f:
                self.label_ohe = pickle.load(f)
        else:
            self.label_ohe = OneHotEncoder(handle_unknown='error')
            self.label_ohe.fit(np.expand_dims(np.array(classes_list), -1))
            logger.info(f'Categories: {self.label_ohe.categories_}')
            logger.info(f'Saving LABEL OHE to {LABEL_OHE}')
            with open(LABEL_OHE, 'wb') as f:
                pickle.dump(self.label_ohe, f)
        
        self.labels_text = self.dataset[['label_text']]
        self.labels = self.label_ohe.transform(self.labels_text.values)

        encoded_columns_list = [
            'tag_name', 
            'tag_name_parent', 
            'attr_role', 
            'attr_role_parent', 
            'attr_type', 
            'attr_type_parent', 
            'label', 
            'label_text'
        ]
        logger.info(f'Drop encoded columns: [{encoded_columns_list}]')
        self.dataset.drop(columns=encoded_columns_list, inplace=True)
        self.data = hstack([self.dataset.values.astype(np.float32), self.sm])

    def rebalance(self):
        """
            Make the dataset balanced
        """
        logger.info('Rebalance dataset')
        class_counts = [ r for r in self.dataset.label.value_counts().sort_values(ascending=False).items()]
        max_count = class_counts[0][1]

        dfs = [self.dataset]
        for cc in class_counts[1:]:
            ratio = max_count//cc[1]
            ratio = 10 if ratio >= 10 else ratio
            for _ in range(ratio):
                dfs.append(self.dataset[self.dataset.label == cc[0]].copy())

        self.dataset = pd.concat(dfs)
        logger.info(f'Rebalanced dataset size: {self.dataset.shape[0]}')

    def __len__(self):
        return self.data.shape[0]

    def __getitem__(self, idx):
        return np.array(self.data.getrow(idx).todense()[0]).squeeze(), np.array(self.labels.getrow(idx).todense()[0]).squeeze()

    def _find_dataset_names(self, path_mask='dataset/df/*.parquet'):
        return  set([re.sub( '.*[/\\\]', '', re.sub('\\..*$', '', os.path.normpath(fn)))
                    for fn in glob.glob(path_mask)])

    def _gen_dataset_names(self):
        dfs = self._find_dataset_names('dataset/df/*.parquet')
        imgs = self._find_dataset_names('dataset/images/*.png')
        anns = self._find_dataset_names('dataset/annotations/*.txt')

        return (dfs.intersection(imgs)).intersection(anns)

        


