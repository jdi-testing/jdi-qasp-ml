import os

from vars.path_vars import (
    UPLOAD_DIRECTORY,
    TEMPLATES_PATH,
    MODEL_VERSION_DIRECTORY,
    JS_DIRECTORY,
    mui_df_path,
    mui_model,
    old_df_path,
    old_model,
    redis_address
)

prefix = os.getcwd().split("jdi-qasp-ml")[0]

REDIS_URL = os.getenv('REDIS_ADDRESS', redis_address)
BASE_DIR = os.path.join(prefix, "jdi-qasp-ml")

UPLOAD_DIRECTORY = os.getenv('UPLOAD_DIRECTORY', os.path.join(BASE_DIR, UPLOAD_DIRECTORY))
TEMPLATES_PATH = os.getenv('TEMPLATES_PATH', os.path.join(BASE_DIR, TEMPLATES_PATH))
MODEL_VERSION_DIRECTORY = os.getenv('MODEL_VERSION_DIRECTORY', os.path.join(BASE_DIR, MODEL_VERSION_DIRECTORY))
JS_DIRECTORY = os.getenv('JS_DIRECTORY', os.path.join(BASE_DIR, JS_DIRECTORY))
mui_df_path = os.getenv('JS_DIRECTORY', os.path.join(BASE_DIR, mui_df_path))
mui_model = os.getenv('JS_DIRECTORY', os.path.join(BASE_DIR, mui_model))
old_df_path = os.getenv('JS_DIRECTORY', os.path.join(BASE_DIR, old_df_path))
old_model = os.getenv('JS_DIRECTORY', os.path.join(BASE_DIR, old_model))
