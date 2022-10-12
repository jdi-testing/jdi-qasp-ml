# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import os
import sys
from glob import glob

import pickle

from multiprocessing import freeze_support

prefix = os.getcwd().split("jdi-qasp-ml")[0]
sys.path.append(os.path.join(prefix, "jdi-qasp-ml"))

from vars.html5_train_vars import (  # noqa
    parameters,  # noqa
    TRAIN_LEN,  # noqa
    TEST_LEN,  # noqa
)  # noqa

from utils.config import logger  # noqa
from utils.dataset import HTML5_JDNDataset  # noqa

from sklearn.tree import DecisionTreeClassifier  # noqa
from sklearn.model_selection import GridSearchCV  # noqa
from sklearn.metrics import classification_report  # noqa

from sklearn import tree  # noqa
import matplotlib.pyplot as plt  # noqa

model_path = os.path.join(prefix, "jdi-qasp-ml", "HTML5_model/model")
df_path = os.path.join(prefix, "jdi-qasp-ml", "data/html5_dataset/df")
classes_path = os.path.join(prefix, "jdi-qasp-ml", "data/html5_dataset/classes.txt")

ds_files = glob(f"{df_path}/html5-*.pkl")
DATASET_NAMES = [os.path.basename(path)[:-4] for path in ds_files]

# train_names = DATASET_NAMES[:TRAIN_LEN]y
# test_names = DATASET_NAMES[TRAIN_LEN : TRAIN_LEN + TEST_LEN]  # noqa

train_names = DATASET_NAMES[TEST_LEN: (TRAIN_LEN + TEST_LEN)]
test_names = DATASET_NAMES[:TEST_LEN]


if __name__ == "__main__":

    freeze_support()

    train_dataset = HTML5_JDNDataset(
        datasets_list=train_names, dataset_type="html5", rebalance_and_shuffle=False
    )
    test_dataset = HTML5_JDNDataset(
        datasets_list=test_names, dataset_type="html5", rebalance_and_shuffle=False
    )

    logger.info(
        f"Train dataset shape:  {train_dataset.X.shape}; Test dataset shape: {test_dataset.X.shape}"
    )

    with open(classes_path, "r",) as f:
        lines = f.readlines()
        encoder_dict = {line.strip(): i for i, line in enumerate(lines)}
        decoder_dict = {v: k for k, v in encoder_dict.items()}

    print("WARNING: Create new model")

    best_accuracy = 0.0

    logger.info(f"START TRAINING THE MODEL WITH THE BEST ACCURACY: {best_accuracy}")

    model = GridSearchCV(DecisionTreeClassifier(), parameters, n_jobs=4)
    model.fit(X=train_dataset.X, y=train_dataset.y)
    model = model.best_estimator_

    logger.info("Classification report for train set:")
    logger.info(
        classification_report(
            train_dataset.y,
            model.predict(train_dataset.X),
            target_names=list(encoder_dict.keys()),
        )
    )

    y_pred = model.predict(test_dataset.X)

    logger.info("Classification report for test set:")
    logger.info(
        classification_report(
            test_dataset.y, y_pred, target_names=list(encoder_dict.keys())
        )
    )

    save_or_not = input("Do you want to save that model? (Y/N):  ")
    if save_or_not in ["Y", "y"]:
        pkl_filename = "DT_model.pkl"
        with open(f"{model_path}/{pkl_filename}", "wb") as file:
            pickle.dump(model, file)

        fig = plt.figure(figsize=(100, 50))
        _ = tree.plot_tree(
            model,
            feature_names=train_dataset.X.columns,
            class_names=list(encoder_dict.keys()),
            filled=True,
        )
        plt.savefig(f"{model_path}/tree.jpeg", format="jpeg", bbox_inches="tight")
    exit(0)
