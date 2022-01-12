import sys

import pandas as pd

from selenium.webdriver.common.keys import Keys

import re
import os

from time import sleep
from .common import maximize_window

from .config import logger

prefix = os.getcwd().split("jdi-qasp-ml")[0]
sys.path.append(os.path.join(prefix, "jdi-qasp-ml"))

js_path = os.path.join(prefix, "jdi-qasp-ml", "js")


def followers_features(
    df: pd.DataFrame, followers_set: set = None, level=0
) -> pd.DataFrame:
    """
        Build feature: "children_tags" and max reverse depth ( depth from leafs)
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


class DatasetBuilder:
    """
        Build dataset from a specific url,

    """

    headless = True

    def __init__(
        self,
        url: str,
        dataset_name: str = "dummy",
        headless=True,
        dataset_root_path="./dataset/",
    ):

        if dataset_name == "dummy":
            logger.warning('The default dataset name "dummy" will be used')
        else:
            logger.info(f"Dataset name: {dataset_name}")

        super(DatasetBuilder).__init__()
        self.url = url
        self.driver = None
        self.logger = logger
        self.dataset_name = dataset_name
        self.headless = headless
        self.root_path = dataset_root_path.rstrip("/")

        logger.info("Create directories to save the dataset")
        # logger.info('dataset/images')
        os.makedirs(f"{self.root_path}/images", exist_ok=True)
        # logger.info('dataset/df')
        os.makedirs(f"{self.root_path}/df", exist_ok=True)
        # logger.info('dataset/annotations')
        os.makedirs(f"{self.root_path}/annotations", exist_ok=True)
        # logger.info('dataset/html')
        os.makedirs(f"{self.root_path}/html", exist_ok=True)
        # logger.info('dataset/cache-labels')
        os.makedirs(f"{self.root_path}/cache-labels", exist_ok=True)

        self.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("Close web driver")
        self.driver.close()

    def __enter__(self):
        import selenium
        from selenium.webdriver.chrome.options import Options

        if self.driver is not None:
            return self

        self.options = Options()
        # Last I checked this was necessary.
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--skip-js-errors")

        # to prevent "I'm not a robot" check, we have to add next option:
        self.options.add_argument(
            '--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/95.0.4638.54 Safari/537.36")'
        )  # noqa
        if sys.platform != "darwin":
            self.options.set_capability("platformName", "windows")
        # self.options.add_argument("--start-maximized")
        if self.headless:
            self.options.add_argument("--headless")

        logger.info("Creating driver")
        if sys.platform == "darwin":
            chrome_driver_path = "/usr/local/bin/chromedriver"
        else:
            chrome_driver_path = os.path.join(os.getcwd(), "chromedriver.exe")
        if os.path.exists(chrome_driver_path):
            self.driver = selenium.webdriver.Chrome(
                executable_path=chrome_driver_path, options=self.options
            )
        else:
            raise FileNotFoundError(f"chromedriver.exe  {os.getcwd()}")

        logger.info("Chrome web driver is created")
        self.setUp(self.driver)
        scr = f"{self.root_path}/images/{self.dataset_name}.png"
        logger.info(f"save scrinshot: {scr}")
        self.driver.save_screenshot(scr)
        self.build_dataset()

        return self

    def full_page(self, driver):
        logger.info("Getting full page")
        sleep(3.0)
        html_e = driver.find_element_by_tag_name("html")
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
        logger.info(f"getting url: {self.url}")
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

        logger.info("Collect features using JS script")
        with open(f"{js_path}/build-dataset.js", "r") as f:
            build_dataset_js = f.read()

        self.dataset_json = self.driver.execute_script(build_dataset_js)
        self.dataset = pd.DataFrame(self.dataset_json)

        # Save HTML source
        logger.info(f"Save html to {self.root_path}/html/{self.dataset_name}.html")
        with open(f"{self.root_path}/html/{self.dataset_name}.html", "wb") as f:
            f.write(self.driver.page_source.encode())
            f.flush()

        self.dataset.onmouseover = self.dataset.onmouseover.apply(
            lambda x: "true" if x is not None else None
        )
        self.dataset.onmouseenter = self.dataset.onmouseenter.apply(
            lambda x: "true" if x is not None else None
        )

        logger.info(f"Save peakle to {self.root_path}/df/{self.dataset_name}.pkl")

        logger.info(
            "No attributes: " + str(self.dataset[self.dataset.attributes == {}].shape)
        )

        self.dataset.attributes = self.dataset.attributes.apply(
            lambda x: None if x == {} else x
        )

        self.dataset.to_pickle(f"{self.root_path}/df/{self.dataset_name}.pkl")

        return self.dataset


logger.info("dataset package is loaded...")
