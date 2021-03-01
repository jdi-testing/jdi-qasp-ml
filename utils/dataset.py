import numba
import pandas as pd
import numpy as np
import selenium
from selenium.webdriver.chrome.options import Options
from .common import iou_xywh
from tqdm.auto import tqdm, trange
import os, sys
import logging
from time import sleep
from collections import Counter

from .common import TQDM_BAR_FORMAT, get_all_elements, maximize_window, screenshot, build_elements_dataset
from .config import logger

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


def build_parent_features(elements_df:pd.DataFrame) -> pd.DataFrame:
    
    parents_set = set(elements_df.parent_id.values) # take all elements which have children

    logger.info('Building "parent_width"')
    parents_width_dict = dict(elements_df[elements_df.element_id.isin(parents_set)][['element_id', 'width']].values)
    elements_df['parent_width'] = elements_df.parent_id.map(parents_width_dict).fillna(0.0)

    logger.info('Building "parent_height"')
    parents_height_dict = dict(elements_df[elements_df.element_id.isin(parents_set)][['element_id', 'height']].values)
    elements_df['parent_height'] = elements_df.parent_id.map(parents_height_dict).fillna(0.0)

    logger.info('Building "parent_tag_name"')
    parents_tag_dict = dict(elements_df[elements_df.element_id.isin(parents_set)][['element_id', 'tag_name']].values)
    elements_df['parent_tag_name'] = elements_df.parent_id.map(parents_tag_dict).fillna('html')

    logger.info('Building "parent_is_hover"')
    parents_is_hover_dict = dict(elements_df[elements_df.element_id.isin(parents_set)][['element_id', 'is_hover']].values)
    elements_df['parent_is_hover'] = elements_df.parent_id.map(parents_is_hover_dict).fillna(False).astype(int)

    logger.info('Building "parent_displayed"')
    parents_displayed_dict = dict(elements_df[elements_df.element_id.isin(parents_set)][['element_id', 'displayed']].values)
    elements_df['parent_displayed'] = elements_df.parent_id.map(parents_displayed_dict).fillna(False).astype(int)

    elements_df.is_hover = elements_df.is_hover.astype(int)
    elements_df.displayed = elements_df.displayed.astype(int)

    return elements_df



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
        






