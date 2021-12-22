import os
import sys
import re
from glob import glob
from time import sleep

prefix = os.getcwd().split("jdi-qasp-ml")[0]
dataset_path = os.path.join(prefix, "jdi-qasp-ml", "data/html5_dataset")

sys.path.append(os.path.join(prefix, "jdi-qasp-ml"))

from utils.config import logger  # noqa

from utils.dataset_builder import DatasetBuilder  # noqa
from utils.common import maximize_window  # noqa

os.makedirs(dataset_path, exist_ok=True)

WAIT_TIME_SECONDS = 3

SITE_URLS = [
    "file://" + p
    for p in glob(
        f'{os.path.join(prefix, "jdi-qasp-ml")}/data/html5_dataset/build/*.html'
    )
]
DATASET_NAMES = ["html5-" + re.search("[0-9]+.html", nm)[0][:-5] for nm in SITE_URLS]


class JDIDatasetBuilder(DatasetBuilder):
    def setUp(self, driver):
        self.logger.info("getting page")
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
