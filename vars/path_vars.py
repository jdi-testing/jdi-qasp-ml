# paths for using in train

dataset_dict = {
    "mui": "data/mui_dataset",
    "html5": "data/html5_dataset",
    "bs": "data/bs_dataset",
    "angular": "data/angular_dataset",
    "vuetify": "data/vuetify_dataset"
}

model_dict = {
    "mui": "MUI_model/model",
    "html5": "HTML5_model/model",
    "bs": "BS_model/model",
    "angular": "Angular_model/model",
    "vuetify": "Vuetify_model/model"
}

# paths for using in main.py
UPLOAD_DIRECTORY = "data/uploaded_dataset/df"
ANGULAR_UPLOAD_DIRECTORY = "data/angular_dataset/df"
TEMPLATES_PATH = "templates"
MODEL_VERSION_DIRECTORY = "model/version"
JS_DIRECTORY = "js"

html5_classes_path = "data/html5_dataset/classes.txt"

mui_df_path = "data/mui_dataset/df"
old_df_path = "data/old_dataset/df"
angular_df_path = "data/angular_dataset/df"
old_model = "Old_model/model"
mui_model = "MUI_model/model"
html5_df_path = "data/html5_dataset/df"
html5_model = "HTML5_model/model"
angular_model = "Angular_model/model"
vuetify_model = "Vuetify_model/model"

redis_address = "redis://redis:6379"
