import os


REDIS_ADDRESS = os.getenv('REDIS_ADDRESS', 'redis://redis:6379')

UPLOAD_DIRECTORY = os.getenv('UPLOAD_DIRECTORY', 'dataset/df')
MODEL_VERSION_DIRECTORY = os.getenv('MODEL_VERSION_DIRECTORY', 'model/version')
JS_DIRECTORY = os.getenv('JS_DIRECTORY', 'js')
