import os
# from IPython.display import display
import pandas as pd
import numpy as np
from MUI_model.utils.config import logger
# from .common import iou_xywh
from tqdm.auto import tqdm
from collections import defaultdict
# from datetime import datetime
# import re
# import pickle


def assign_labels(df: pd.DataFrame, 
                  classes_file_path: str = 'dataset/classes.txt', verbose=False) -> pd.DataFrame:

    with open(classes_file_path, 'r') as f:
        lines = f.readlines()
        encoder_dict = {line.strip(): i for i, line in enumerate(lines)}
        logger.info(str(encoder_dict))
        decoder_dict = {v: k for k, v in encoder_dict.items()}
      

    if len(encoder_dict) != len(decoder_dict):
        msg = f'There are duplicate key/values in the {classes_file_path}'
        logger.fatal(msg)
        raise Exception(msg)

    def labels(label_text, encoder_dict):
        encoded_label = encoder_dict[label_text]
        return encoded_label
    
    vec_labels = np.vectorize(labels, excluded=['encoder_dict'])
        
    df['label'] = vec_labels(df['label_text'], encoder_dict)
    # remove duplicates
    df = df.sort_values(by=['element_id', 'parent_id'])
    df = df[~df[['element_id', 'parent_id']].duplicated(keep='last')].copy()
    

    return df
