# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import os
import sys
import gc
from tqdm.auto import trange
import pandas as pd
from glob import glob

from sys import argv


import torch
from torch.utils.data import DataLoader

from multiprocessing import freeze_support
from terminaltables import DoubleTable

prefix = os.getcwd().split("jdi-qasp-ml")[0]
sys.path.append(os.path.join(prefix, "jdi-qasp-ml"))

from vars.train_vars import (  # noqa
    BATCH_SIZE,  # noqa
    TRAIN_LEN,  # noqa
    TEST_LEN,  # noqa
    NUM_EPOCHS,  # noqa
    EARLY_STOPPING_THRESHOLD,  # noqa
    SCHEDULER_STEP,  # noqa
)  # noqa

from utils.config import logger  # noqa
from utils.dataset import JDNDataset  # noqa
from utils.model_new import JDIModel  # noqa
from utils.common import accuracy  # noqa

model_path = os.path.join(prefix, "jdi-qasp-ml", "MUI_model/model")
df_path = os.path.join(prefix, "jdi-qasp-ml", "data/mui_dataset/df")

ds_files = glob(f"{df_path}/site*.pkl")
DATASET_NAMES = [os.path.basename(path)[:-4] for path in ds_files]

train_names = DATASET_NAMES[:TRAIN_LEN]
test_names = DATASET_NAMES[TRAIN_LEN : TRAIN_LEN + TEST_LEN]  # noqa

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"device: {DEVICE}")


def evaluate(model: JDIModel, dataset: JDNDataset) -> pd.DataFrame:
    model.eval()
    with torch.no_grad():

        dataloader = DataLoader(dataset, shuffle=False, batch_size=1, pin_memory=True)
        results = []

        with trange(len(dataloader), desc="Evaluating:") as bar:
            with torch.no_grad():
                for x, y in dataloader:
                    y_pred = (
                        torch.round(
                            torch.nn.Softmax(dim=1)(model(x.to(DEVICE)).to("cpu"))
                        )
                        .detach()
                        .numpy()
                    )
                    y_pred = y_pred[0].argmax()
                    y = y.item()

                    results.append(
                        {
                            "y_true": y,
                            "y_pred": y_pred,
                            "y_true_label": dataset.classes_reverse_dict[y],
                            "y_pred_label": dataset.classes_reverse_dict[y_pred],
                        }
                    )
                    bar.update(1)

    results_df = pd.DataFrame(results)
    results_df["is_hidden"] = dataset.df.is_hidden.values
    return accuracy(results_df)


if __name__ == "__main__":

    freeze_support()

    train_dataset = JDNDataset(datasets_list=train_names, rebalance_and_shuffle=True)
    test_dataset = JDNDataset(datasets_list=test_names, rebalance_and_shuffle=False)

    logger.info(
        f"Train dataset shape:  {train_dataset.X.shape}; Test dataset shape: {test_dataset.X.shape}"
    )

    train_dataloader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        pin_memory=True,
        drop_last=True,
        num_workers=0,
    )

    IN_FEATURES = next(iter(train_dataloader))[0][0].shape[0]
    OUT_FEATURES = len(train_dataset.classes_dict)

    if os.path.exists(f"{model_path}/model.pth"):
        print("WARNING: load saved model weights")
        model = torch.load(f"{model_path}/model.pth", map_location="cpu").to(DEVICE)
        best_accuracy = evaluate(model=model, dataset=test_dataset)
    else:
        print("WARNING: Create brand new model")
        model = JDIModel(in_features=IN_FEATURES, out_features=OUT_FEATURES)
        best_accuracy = 0.0

    logger.info(f"START TRAINING THE MODEL WITH THE BEST ACCURACY: {best_accuracy}")

    # just for test purpose:
    # model = JDIModel(in_features=IN_FEATURES, out_features=OUT_FEATURES)

    train_metrics = []
    gc.collect()

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer, step_size=SCHEDULER_STEP, gamma=0.1
    )

    NUM_BATCHES = len(train_dataloader)

    early_stopping_steps = EARLY_STOPPING_THRESHOLD

    for epoch in range(NUM_EPOCHS):

        model.train()
        model.to(DEVICE)

        cumulative_loss = 0.0
        cumulative_main_loss = 0.0

        with trange(NUM_BATCHES) as bar:

            for x, y in train_dataloader:
                y_hat = model(x.to(DEVICE))

                optimizer.zero_grad()

                loss = criterion(y_hat, y.long().to(DEVICE))  # \ noqa

                loss.backward()
                optimizer.step()
                cumulative_loss += loss.item()
                bar.set_description(
                    f"Epoch: {epoch}, {round(cumulative_loss,5)}, {round(loss.item(),5)}"
                )  # noqa
                bar.update(1)

            bar.update(1)

        early_stopping_steps -= 1
        test_accuracy = evaluate(model=model, dataset=test_dataset)
        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            logger.info(f"SAVING MODEL WITH THE BEST ACCURACY: {best_accuracy}")
            torch.save(model, f"{model_path}/model.pth")
            early_stopping_steps = EARLY_STOPPING_THRESHOLD

        train_metrics.append(
            {
                "epoch": epoch,
                "mean(loss)": cumulative_loss / NUM_BATCHES,
                "accuracy(test)": test_accuracy,
            }
        )

        # report metrics
        print()
        table_data = [["epoch", "mean(loss)", "accuracy(test)"]]
        for r in train_metrics:
            table_data.append([r["epoch"], r["mean(loss)"], r["accuracy(test)"]])

        print(DoubleTable(table_data=table_data).table)
        print(f"Best accuracy: {best_accuracy}, attempts left: {early_stopping_steps}")

        if early_stopping_steps <= 0:
            logger.info("EARLY STOPPING")
            break
        scheduler.step()

    pd.DataFrame(train_metrics, index=list(range(len(train_metrics)))).to_csv(
        "tmp/train_metrics.csv"
    )
    exit(0)
