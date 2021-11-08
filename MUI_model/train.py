# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import os
import gc
import sys
from tqdm.auto import trange
import pandas as pd

import torch
from torch.utils.data import DataLoader


sys.path.append('.')
# print(os.getcwd())

from MUI_model.utils.config import logger  # noqa
from MUI_model.utils.dataset import JDNDataset  # noqa
from MUI_model.utils.model import JDIModel  # noqa
from MUI_model.utils.common import accuracy  # noqa

from multiprocessing import freeze_support  # noqa
from terminaltables import DoubleTable  # noqa

BATCH_SIZE = 256

n_datasets = 120

DATASET_NAMES = [f'mui-site{i}' for i in range(1, n_datasets+1)]

ds_files = [f'/MUI_model/dataset/df/{fn}.pkl' for fn in DATASET_NAMES]

train_names = DATASET_NAMES[:100]
test_names = DATASET_NAMES[100:]

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
logger.info(f'device: {DEVICE}')


def evaluate(model: JDIModel, dataset: JDNDataset) -> pd.DataFrame:
    model.eval()
    with torch.no_grad():

        dataloader = DataLoader(dataset, shuffle=False, batch_size=1, pin_memory=True)
        results = []

        with trange(len(dataloader), desc='Evaluating:') as bar:
            with torch.no_grad():
                for x, y in dataloader:
                    y_pred = torch.round(torch.nn.Softmax(dim=1)(model(x.to(DEVICE)).to('cpu'))).detach().numpy()
                    y_pred = y_pred[0].argmax()
                    y = y.item()

                    results.append({
                        'y_true': y,
                        'y_pred': y_pred,
                        'y_true_label': dataset.classes_reverse_dict[y],
                        'y_pred_label': dataset.classes_reverse_dict[y_pred]
                    })
                    bar.update(1)

    results_df = pd.DataFrame(results)
    results_df['is_hidden'] = dataset.df.is_hidden.values
    return accuracy(results_df)


if __name__ == "__main__":

    freeze_support()

    train_dataset = JDNDataset(datasets_list=train_names, rebalance_and_shuffle=True)
    # train_dataset = JDNDataset(datasets_list=None, rebalance_and_suffle=True)
    test_dataset = JDNDataset(datasets_list=test_names, rebalance_and_shuffle=False)

    logger.info(f'Train dataset shape:  {train_dataset.X.shape}; Test dataset shape: {test_dataset.X.shape}')

    train_dataloader = DataLoader(train_dataset,
                                  batch_size=BATCH_SIZE,
                                  shuffle=True,
                                  pin_memory=True,
                                  drop_last=True,
                                  num_workers=0)

    IN_FEATURES = next(iter(train_dataloader))[0][0].shape[0]
    OUT_FEATURES = len(train_dataset.classes_dict)

    if os.path.exists('MUI_model/model/model.pth'):
        print('WARNING: load saved model weights')
        model = torch.load('MUI_model/model/model.pth', map_location='cpu').to(DEVICE)
        best_accuracy = evaluate(model=model, dataset=test_dataset)
    else:
        print('WARNING: Create brand new model')
        model = JDIModel(in_features=IN_FEATURES, out_features=OUT_FEATURES)
        best_accuracy = 0.0

    logger.info(f'START TRAINING THE MODEL WITH THE BEST ACCURACY: {best_accuracy}')

    # just for test purpose:
    # model = JDIModel(in_features=IN_FEATURES, out_features=OUT_FEATURES)

    train_metrics = []
    lambda_input = .01
    lambda_hidden = .0001
    gc.collect()

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    NUM_BATCHES = len(train_dataloader)
    NUM_EPOCS = 90
    EARLY_STOPPING_THRESHOLD = 20
    early_stopping_steps = EARLY_STOPPING_THRESHOLD

    for epoch in range(NUM_EPOCS):

        model.train()
        model.to(DEVICE)

        cumulative_loss = 0.0
        cumulative_main_loss = 0.0

        with trange(NUM_BATCHES) as bar:

            for x, y in train_dataloader:
                y_hat = model(x.to(DEVICE))

                optimizer.zero_grad()

                main_loss = criterion(y_hat, y.long().to(DEVICE))

                loss = main_loss   # \ noqa
                # + torch.abs(model.input_layer.weight).sum()*lambda_input \ noqa
                # + (model.hidden1.weight**2).sum()*lambda_hidden \ noqa
                # + (model.hidden2.weight**2).sum()*lambda_hidden noqa

                loss.backward()
                optimizer.step()
                cumulative_loss += loss.item()
                cumulative_main_loss += main_loss.item()
                bar.set_description(f"Epoch: {epoch}, {round(cumulative_loss,5)}, {round(main_loss.item(),5)}, {round(loss.item(),5)}") # noqa
                bar.update(1)

            bar.update(1)

        # evaluate model
        # torch.save(model, f'model/model-{epoch}.pth')
        early_stopping_steps -= 1
        test_accuracy = evaluate(model=model, dataset=test_dataset)
        if test_accuracy > best_accuracy:
            best_accuracy = test_accuracy
            logger.info(f'SAVING MODEL WITH THE BEST ACCUCACY: {best_accuracy}')
            torch.save(model, 'MUI_model/model/model.pth')
            early_stopping_steps = EARLY_STOPPING_THRESHOLD

        train_metrics.append({
            'epoch': epoch,
            'mean(loss)': cumulative_loss / NUM_BATCHES,
            # 'loss': cumulative_main_loss / NUM_BATCHES,
            'accuracy(test)': test_accuracy
        })

        # report metrics
        print()
        # table_data = [['epoch', 'mean(loss)', 'loss', 'accuracy(test)']]
        table_data = [['epoch', 'mean(loss)', 'accuracy(test)']]
        for r in train_metrics:
            # table_data.append([r['epoch'], r['mean(loss)'], r['loss'], r['accuracy(test)']])
            table_data.append([r['epoch'], r['mean(loss)'], r['accuracy(test)']])

        print(DoubleTable(table_data=table_data).table)
        print(f'Best accuracy: {best_accuracy}, attempts left: {early_stopping_steps}')

        if early_stopping_steps <= 0:
            logger.info('EARLY STOPPING')
            exit(0)
