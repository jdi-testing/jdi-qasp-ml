import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()

prefix = os.getcwd().split("jdi-qasp-ml")[0]
sys.path.append(os.path.join(prefix, "jdi-qasp-ml"))

UTILS_LOGGER = "utils.dataset"
LOG_DIR_PATH = os.path.join(os.getcwd(), "tmp")
LOG_FILE_PATH = os.path.join(os.getcwd(), "tmp/log.txt")

os.makedirs(LOG_DIR_PATH, exist_ok=True)

logger = logging.getLogger(UTILS_LOGGER)
logger.setLevel(logging.DEBUG)


formatter = logging.Formatter(
    "%(asctime)s -%(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(filename=LOG_FILE_PATH, mode="w")
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

EMAIL_SENDER_LOGIN = os.getenv("EMAIL_SENDER_LOGIN", "SpiridonovFed@yandex.ru")
EMAIL_SENDER_PASSWORD = os.getenv("EMAIL_SENDER_PASSWORD")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.yandex.ru")
RECIPIENT_EMAILS = os.getenv("RECIPIENT_EMAILS", "SupportJDI@epam.com")

SELENOID_PARALLEL_SESSIONS_COUNT = int(
    os.getenv("SELENOID_PARALLEL_SESSIONS_COUNT", len(os.sched_getaffinity(0)))
)

logger.info("Module utils.config was loaded")
