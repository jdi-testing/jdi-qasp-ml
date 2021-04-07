import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os, sys, re, gc, glob
from tqdm.auto import tqdm, trange
from utils import logger
from utils.model import JDIModel
from multiprocessing import freeze_support
from terminaltables import DoubleTable

from utils import DatasetBuilder, \
                  JDIDataset, \
                  maximize_window, \
                  assign_labels, \
                  build_tree_features, \
                  build_children_features, \
                  build_elements_dataset

from time import sleep

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import OneHotEncoder

import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

BATCH_SISE = 256

if __name__ == "__main__":
    freeze_support()

    train_dataset = JDIDataset(rebalance=True)
    logger.info(f' Dataset shapes:  {train_dataset.dataset.shape}, {train_dataset.data.shape}')

    train_dataloader = DataLoader(train_dataset, 
                                  batch_size=BATCH_SISE, 
                                  shuffle=True, 
                                  collate_fn = train_dataset.collate_fn, 
                                  pin_memory=True,
                                  drop_last=True,
                                  num_workers=0)
    
    IN_FEATURES = next(iter(train_dataloader))[0][0].shape[0]
    OUT_FEATURES = len(train_dataset.classes_dict)

    if os.path.exists('model/model.pth'):
        print('WARNING: load saved model weights')
        model = torch.load('model/model.pth')
    else:
        print('WARNING: Create brand new model')    
        model = JDIModel(in_features=IN_FEATURES, out_features=OUT_FEATURES)
    # model = JDIModel(in_features=IN_FEATURES, out_features=OUT_FEATURES)

    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info(f'device: {DEVICE}')

    stats = []
    lambda_input  = .01
    lambda_hidden = .0001
    gc.collect()

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

    NUM_BATCHES = len(train_dataloader)
    NUM_EPOCS = 30

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

                loss = main_loss #\
                    # + torch.abs(model.input_layer.weight).sum()*lambda_input \
                    # + (model.hidden1.weight**2).sum()*lambda_hidden \
                    # + (model.hidden2.weight**2).sum()*lambda_hidden
                
                loss.backward()
                optimizer.step()
                cumulative_loss += loss.item()
                cumulative_main_loss += main_loss.item()
                bar.set_description(f"Epoch: {epoch}, {round(cumulative_loss,5)}, {round(main_loss.item(),5)}, {round(loss.item(),5)}")
                bar.update(1)

            bar.update(1)

            stats.append({
                'epoch': epoch,
                'mean(loss)': cumulative_loss/NUM_BATCHES,
                'loss': cumulative_main_loss/NUM_BATCHES
            })
            sleep(1)
            print()
            table_data = [['epoch', 'mean(loss)', 'loss']]
            for r in stats:
                table_data.append([r['epoch'], r['mean(loss)'], r['loss']])
            print(DoubleTable(table_data=table_data).table)
            print()


        model.eval()
        with torch.no_grad():
            #torch.save(model, f'model/model-{epoch}.pth')
            torch.save(model, 'model/model.pth')

