import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
from IPython.display import HTML
from IPython.display import display as ipython_displpay
from selenium.webdriver.common.by import By
from sklearn.metrics import confusion_matrix
from collections import Counter

import numba

from .config import logger

TQDM_BAR_FORMAT = "{desc:25}{percentage:3.0f}%|{bar:50}{r_bar}"


# Maximize window
def maximize_window(driver=None, extend_pix=0):
    def S(X):
        return driver.execute_script("return document.body.parentNode.scroll" + X)

    driver.set_window_size(width=S("Width"), height=S("Height") + extend_pix)
    driver.find_element(By.TAG_NAME, "body")
    logger.info("Window maximized")


@numba.jit
def iou_xywh(box_a, box_b):
    """ Compute Intersection over Union (IoU)
        a box should be a tuple (x, y, width, height)

        Example:
        >>>  assert round( \
                 iou_xywh( \
                     (10, 20, 30, 50), \
                     (30, 50, 50, 40)),6)==0.060606, \
            f"Expected: 0.060606, but {iou_xywh((10, 20, 30, 50), \
                                                (30, 50, 50, 40))} \
                                                    was returned"
    """

    x1, y1, w1, h1 = box_a
    x2, y2, w2, h2 = box_b

    if x1 + w1 <= x2:
        return 0.0
    if x2 + w2 <= x1:
        return 0.0
    if y1 + h1 <= y2:
        return 0.0
    if y2 + h2 <= y1:
        return 0.0

    if (w1 <= 0.0) or (w2 <= 0.0) or (h1 <= 0.0) or (h2 <= 0.0):
        return 0.0

    s1 = w1 * h1
    s2 = w2 * h2

    si = (min(x1 + w1, x2 + w2) - max(x1, x2)) * (min(y1 + h1, y2 + h2) - max(y1, y2))

    return si / (s1 + s2 - si)


def build_tree_dict(df: pd.DataFrame) -> dict:
    """
        Builds tree dict for
        get_parents_list
        df:pd.DataFrame must have columns: 'parent_id', 'element_id'

    """
    # tree_dict = dict(zip(df.element_id.values, df.parent_id.values))  # old implementation
    tree_dict = {
        r.element_id: None if r.element_id == r.parent_id else r.parent_id
        for _, r in df[["element_id", "parent_id"]].iterrows()
    }

    return tree_dict


def accuracy(
    df: pd.DataFrame,
    y_true: str = "y_true_label",
    y_pred: str = "y_pred_label",
    verbose: bool = True,
    dummy: str = "n/a",
):
    """
        Calculates accuracy on all elements which are not "n/a"
        Parameters: y_true, y_pred are column names
    """
    total_cnt = df.shape[0]
    df = df[[y_true, y_pred]][
        ((df[y_true] != dummy) | (df[y_pred] != dummy))
    ]
    n = df.shape[0]

    if n != 0:
        true_cnt = df[df[y_true] == df[y_pred]].shape[0]
        acc = true_cnt / n
        if verbose:
            ipython_displpay(HTML(f"<H2>Accuracy: {acc} <H2>"))
            logger.info(f"Accuracy:  {true_cnt}/{n} = {acc}, for {total_cnt} elements")
        return acc

    else:
        ipython_displpay("<h1>Exception: No predictions<h1>")
        logger.info("<h1>Exception: No predictions<h1>")
        raise Exception("No predictions")

    return None


def accuracy_each_class(
    df: pd.DataFrame,
    y_true: str = "y_true_label",
    y_pred: str = "y_pred_label",
    verbose: bool = True,
    dummy: str = "n/a",
):
    """
        Calculates accuracy for each class on all elements which are not "n/a"
        Parameters: y_true, y_pred are column names
    """
    with open('data\\vuetify_dataset\\classes.txt') as f:
        classes = f.readlines()
    df = df[(df['y_true'] != dummy) | (df['y_pred'] != dummy)]
    y_true = df['y_true'].to_numpy()
    y_pred = df['y_pred'].to_numpy()
    m = confusion_matrix(y_true, y_pred)
    for a, i in enumerate(m):
        for b, j in enumerate(i):
            if j != 0 and j not in m.diagonal():
                print(f'Class {classes[a]} recognized as {classes[b]} {m[a][b]} time(s)')
    classes_acc = {}
    for n, i in enumerate(m.diagonal()):
        classes_acc[n] = i / Counter(list(y_true))[n]
    if verbose:
        logger.info(f"Accuracy for each class:  {classes_acc}")
    return classes_acc


def load_gray_image(file_path: str) -> np.ndarray:
    img = plt.imread(file_path)
    img = (img[..., 0] + img[..., 1] + img[..., 2]) / 3.0
    return img


logger.info("Module utils.common is loaded...")
