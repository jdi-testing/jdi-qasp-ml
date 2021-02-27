import logging
import sys

UTILS_DATASET_LOGGER  = 'utils.dataset'

logger = logging.getLogger(UTILS_DATASET_LOGGER)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s:%(filename)s:%(lineno)d - %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
