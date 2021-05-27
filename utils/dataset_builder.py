
import pandas as pd

from selenium.webdriver.common.keys import Keys

import re
import os

from time import sleep
from .common import maximize_window

from .config import logger


def followers_features(df: pd.DataFrame, followers_set: set = None, level=0) -> pd.DataFrame:
    """
        Build feature: "children_tags" and max reverse depth ( depth from leafs)
        Concatenate all children tag_names into a string filed 'children_tags'
    """
    # get leafs (nodes without children)
    if followers_set is None:
        level = 0
        followers_set = set(df.element_id.values) - set(df.parent_id.values)
        followers_tags_df = df[df.element_id.isin(followers_set)][['parent_id', 'tag_name']]\
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
        followers_tags_df = df[df.element_id.isin(followers_set)][['parent_id', 'tag_name']]\
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


class DatasetBuilder:
    """
        Build dataset from a specific url,

    """

    headless = True

    def __init__(self, url: str, dataset_name: str = 'dummy', headless=True):

        if dataset_name == 'dummy':
            logger.warning('The default dataset name "dummy" will be used')
        else:
            logger.info(f'Dataset name: {dataset_name}')

        super(DatasetBuilder).__init__()
        self.url = url
        self.driver = None
        self.logger = logger
        self.dataset_name = dataset_name
        self.headless = headless

        logger.info('Create directories to save the dataset')
        # logger.info('dataset/images')
        os.makedirs('dataset/images', exist_ok=True)
        # logger.info('dataset/df')
        os.makedirs('dataset/df', exist_ok=True)
        # logger.info('dataset/annotations')
        os.makedirs('dataset/annotations', exist_ok=True)
        # logger.info('dataset/html')
        os.makedirs('dataset/html', exist_ok=True)

        self.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info('Close web driver')
        self.driver.close()

    def __enter__(self):
        import selenium
        from selenium.webdriver.chrome.options import Options

        if self.driver is not None:
            return self

        self.options = Options()
        # Last I checked this was necessary.
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--skip-js-errors')

        # to prevent "I'm not a robot" check, we have to add next option:
        self.options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36")') # noqa
        self.options.set_capability("platformName", "windows")
        # self.options.add_argument("--start-maximized")
        if self.headless:
            self.options.add_argument('--headless')

        logger.info('Creating driver')
        chrome_driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
        if os.path.exists(chrome_driver_path):
            self.driver = selenium.webdriver.Chrome(
                executable_path=chrome_driver_path, options=self.options)
        else:
            raise FileNotFoundError(f"chromedriver.exe  {os.getcwd()}")

        logger.info('Chrome web driver is created')
        self.setUp(self.driver)
        scr = f'dataset/images/{self.dataset_name}.png'
        logger.info(f'save scrinshot: {scr}')
        self.driver.save_screenshot(scr)
        self.build_dataset()

        return self

    def full_page(self, driver):
        logger.info('Getting full page')
        sleep(3.0)
        html_e = driver.find_element_by_tag_name('html')
        sleep(3.0)
        html_e.send_keys(Keys.CONTROL, Keys.END)
        sleep(3.0)
        html_e.send_keys(Keys.CONTROL, Keys.END)
        sleep(3.0)

        maximize_window(driver=self.driver, extend_pix=0)

        sleep(9.0)
        html_e.send_keys(Keys.CONTROL, Keys.END)
        sleep(3.0)

    def setUp(self, driver):
        """
            This method may be overwitten if you need to login to the site
            and navigate to a specific url,
            otherwise it just returns
        """
        logger.info(f'getting url: {self.url}')
        self.driver.get(self.url)
        sleep(3.0)

        # As an example:
        # driver.find_element_by_id("user-icon").click()
        # driver.find_element_by_id("name").send_keys(LOGIN)
        # driver.find_element_by_id("password").send_keys(PASSWORD)
        # driver.find_element_by_id("login-button").click()
        # sleep(3.0)
        maximize_window(driver=self.driver, extend_pix=0)

        # self.full_page(driver)

    def build_dataset(self):

        logger.info('Collect features using JS script')
        with open('js/build-dataset.js', 'r') as f:
            build_dataset_js = f.read()

        self.dataset_json = self.driver.execute_script(build_dataset_js)
        self.dataset = pd.DataFrame(self.dataset_json)

        # Save HTML source
        logger.info(f'Save html to dataset/html/{self.dataset_name}.html')
        with open(f'dataset/html/{self.dataset_name}.html', 'wb') as f:
            f.write(self.driver.page_source.encode())
            f.flush()

        self.dataset.onmouseover = self.dataset.onmouseover.apply(
            lambda x: 'true' if x is not None else None)
        self.dataset.onmouseenter = self.dataset.onmouseenter.apply(
            lambda x: 'true' if x is not None else None)

        logger.info(f'Save parquet to dataset/df/{self.dataset_name}.parquet')
        self.dataset.to_parquet(f'dataset/df/{self.dataset_name}.parquet')

        return self.dataset


logger.info("dataset package is loaded...")
