import os

REDIS_URL = os.getenv('REDIS_ADDRESS', 'redis://redis:6379')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_DIRECTORY = os.getenv('UPLOAD_DIRECTORY', os.path.join(BASE_DIR, 'dataset/df'))
TEMPLATES_PATH = os.getenv('TEMPLATES_PATH', os.path.join(BASE_DIR, 'templates'))
MODEL_VERSION_DIRECTORY = os.getenv('MODEL_VERSION_DIRECTORY', os.path.join(BASE_DIR, 'model/version'))
JS_DIRECTORY = os.getenv('JS_DIRECTORY', os.path.join(BASE_DIR, 'js'))
