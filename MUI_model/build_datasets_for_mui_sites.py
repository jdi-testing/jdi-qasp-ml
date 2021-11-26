import logging
from tqdm.auto import trange, tqdm
import sys
import os
import re
from glob import glob
from time import sleep

prefix = os.getcwd().split("jdi-qasp-ml")[0]
sys.path.append(os.path.join(prefix, "jdi-qasp-ml"))

from utils.config import logger

from utils.dataset_builder import DatasetBuilder
from utils.common import maximize_window

dataset_path = os.path.join(prefix, "jdi-qasp-ml", "data/mui_dataset")

WAIT_TIME_SECONDS = 3

SITE_URLS = [
    "file://" + p.replace("\\", "/") + "/index.html"
    for p in glob(f'{os.path.join(prefix, "jdi-qasp-ml")}/data/mui_dataset/build/*')
]
DATASET_NAMES = [re.search("site-[0-9]+", nm)[0] for nm in SITE_URLS]


class JDIDatasetBuilder(DatasetBuilder):
    def setUp(self, driver):
        self.logger.info(f"getting page")
        driver.get(self.url)
        maximize_window(driver=driver)
        sleep(WAIT_TIME_SECONDS)


i = 1
for site, ds_name in zip(SITE_URLS, DATASET_NAMES):
    JDIDatasetBuilder(
        url=site, dataset_name=ds_name, headless=True, dataset_root_path=dataset_path,
    )
    logger.info(f"\n------------\n{len(SITE_URLS)-i} SITES LEFT TO PROCESS!")
    i += 1

