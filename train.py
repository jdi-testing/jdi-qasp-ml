# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
import os, gc
from tqdm.auto import trange
import pandas as pd

import torch
from torch.utils.data import DataLoader

from utils import logger
from utils import JDIDataset
from utils import JDIModel
from utils import accuracy

from multiprocessing import freeze_support
from terminaltables import DoubleTable

BATCH_SISE = 256

TRAIN_DATASETS = [
    'angular',
    'bootstrap-1',
    'bootstrap-form-control',
    'bootstrap-form',
    'bootstrap-forms',
    'bootstrap-reboot',
    'bootstrap',
    'complex-table',
    'contact-form',
    # 'dates',
    "different-elemants",
    'gitlab',
    'google-voice',
    'html-5',
    'login',
    'metals-and-colors',
    # 'mobile-and-html-5',
    'ms-office',
    'ozon',
    'performance',
    'react-ant',
    # 'search',
    # 'support',
    # 'table-with-pages',
    'user-table',
    'wildberries',
    'material-ui-Button Groups',
    'material-ui-Switch',
    'material-ui-Textarea Autosize',
    'material-ui-Progress',
    'material-ui-Radio',
    'material-ui-Buttons',
    'material-ui-Checkbox',
    'material-ui-List',
    'material-ui-Text Field',
    'material-ui-Floating Action Button',
    'material-ui-Slider',
    'material-ui-Select'
]

TEST_DATASETS = [
    'dates',
    'search',
    'support',
    'table-with-pages',
    'mobile-and-html-5'
]

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
logger.info(f'device: {DEVICE}')


def evaluate(model: JDIModel, dataset: JDIDataset) -> pd.DataFrame:

    model.eval()
    with torch.no_grad():

        dataloader = DataLoader(test_dataset,
                                shuffle=False,
                                batch_size=1,
                                collate_fn=dataset.collate_fn,
                                pin_memory=True)

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
    return accuracy(results_df)


if __name__ == "__main__":

    freeze_support()

    train_dataset = JDIDataset(dataset_names=TRAIN_DATASETS, rebalance=True)
    # train_dataset = JDIDataset(dataset_names=None, rebalance=True)
    test_dataset = JDIDataset(dataset_names=TEST_DATASETS, rebalance=False)

    logger.info(f'Train dataset shape:  {train_dataset.dataset.shape}; Test dataset shape: {test_dataset.data.shape}')

    train_dataloader = DataLoader(train_dataset,
                                  batch_size=BATCH_SISE,
                                  shuffle=True,
                                  collate_fn=train_dataset.collate_fn,
                                  pin_memory=True,
                                  drop_last=True,
                                  num_workers=0)

    IN_FEATURES = next(iter(train_dataloader))[0][0].shape[0]
    OUT_FEATURES = len(train_dataset.classes_dict)

    if os.path.exists('model/model.pth'):
        print('WARNING: load saved model weights')
        model = torch.load('model/model.pth')
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
            torch.save(model, 'model/model.pth')
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
        print(f'Best accuracy: {best_accuracy}')

        if early_stopping_steps <= 0:
            logger.info('EARLY STOPPING')
            exit(0)
