import os
import sys

from vars.path_vars import (
    UPLOAD_DIRECTORY,
    TEMPLATES_PATH,
    MODEL_VERSION_DIRECTORY,
    JS_DIRECTORY,
    mui_df_path,
    mui_model,
    old_df_path,
    old_model,
    redis_address,
    html5_df_path,
    html5_model,
    html5_classes_path,
)

prefix = os.getcwd().split("jdi-qasp-ml")[0]
sys.path.append(os.path.join(prefix, "jdi-qasp-ml"))

REDIS_URL = os.getenv("REDIS_ADDRESS", redis_address)
BASE_DIR = os.path.join(prefix, "jdi-qasp-ml")

UPLOAD_DIRECTORY = os.getenv(
    "UPLOAD_DIRECTORY", os.path.join(BASE_DIR, UPLOAD_DIRECTORY)
)
TEMPLATES_PATH = os.getenv("TEMPLATES_PATH", os.path.join(BASE_DIR, TEMPLATES_PATH))
MODEL_VERSION_DIRECTORY = os.getenv(
    "MODEL_VERSION_DIRECTORY", os.path.join(BASE_DIR, MODEL_VERSION_DIRECTORY)
)
JS_DIRECTORY = os.getenv("JS_DIRECTORY", os.path.join(BASE_DIR, JS_DIRECTORY))
mui_df_path = os.getenv("mui_df_path", os.path.join(BASE_DIR, mui_df_path))
mui_model = os.getenv("mui_model", os.path.join(BASE_DIR, mui_model))
old_df_path = os.getenv("old_df_path", os.path.join(BASE_DIR, old_df_path))
old_model = os.getenv("old_model", os.path.join(BASE_DIR, old_model))

html5_df_path = os.getenv("html5_df_path", os.path.join(BASE_DIR, html5_df_path))
html5_model = os.getenv("html5_model", os.path.join(BASE_DIR, html5_model))
html5_classes_path = os.getenv(
    "html5_classes_path", os.path.join(BASE_DIR, html5_classes_path)
)
