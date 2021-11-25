import pandas as pd
from IPython.display import HTML
from IPython.display import display as ipython_displpay

# import matplotlib.pyplot as plt
# from matplotlib.patches import Rectangle
import numba

# from time import sleep
# import selenium
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver import ActionChains

from .config import logger

TQDM_BAR_FORMAT = '{desc:25}{percentage:3.0f}%|{bar:50}{r_bar}'
# MAX_PICT_SIZE_TRESHOLD = 128


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

    si = (min(x1 + w1, x2 + w2) - max(x1, x2)) * \
        (min(y1 + h1, y2 + h2) - max(y1, y2))

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
        for _, r in df[['element_id', 'parent_id']].iterrows()
    }

    return tree_dict


def accuracy(df: pd.DataFrame, y_true: str = 'y_true_label', is_hidden: str = 'is_hidden',
             y_pred: str = 'y_pred_label', verbose: bool = True, dummy: str = 'n/a'):
    """
        Calculates accuracy on all elements which are not "n/a"
        Parameters: y_true, y_pred are column names
    """
    total_cnt = df.shape[0]
    df = df[[y_true, y_pred]][((df[y_true] != dummy) | (df[y_pred] != dummy)) & (df[is_hidden] == 0)]
    n = df.shape[0]

    if n != 0:
        true_cnt = df[df[y_true] == df[y_pred]].shape[0]
        acc = true_cnt / n
        if verbose:
            ipython_displpay(HTML(f'<H2>Accuracy: {acc} <H2>'))
            logger.info(
                f'Accuracy:  {true_cnt}/{n} = {acc}, for {total_cnt} elements')
        return acc

    else:
        ipython_displpay('<h1>Exception: No predictions<h1>')
        logger.info('<h1>Exception: No predictions<h1>')
        raise Exception('No predictions')

    return None


logger.info('Module utils.common is loaded...')
