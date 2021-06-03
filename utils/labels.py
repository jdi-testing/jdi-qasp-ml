import os
from IPython.display import display
import pandas as pd
import numpy as np
from .config import logger
from .common import iou_xywh, from_yolo
from tqdm.auto import tqdm


def assign_labels(df: pd.DataFrame, annotations_file_path: str, img_width: int = 0, img_height: int = 0,
                  classes_file_path: str = 'dataset/classes.txt', verbose=False) -> pd.DataFrame:
    """
        mark up dataset: assign labels
        annotations_file_path: yolo-v3 formatted annotation
        - get image sizes MUST be taken from appropriate image,
          because HTML tag has different size (less then actual image is)
        - get dummy_value from dataset/classes.txt

    """
    logger.info(f'Assign labels from annotation file: {annotations_file_path}')

    logger.info('Getting image size')
    # img_width, img_height = df[df.tag_name=='HTML'][['width', 'height']].head(1).values[0]
    logger.info(f'Image size: {(img_width, img_height)}')

    with open(classes_file_path, 'r') as f:
        lines = f.readlines()
        encoder_dict = {line.strip(): i for i, line in enumerate(lines)}
        logger.info(str(encoder_dict))
        decoder_dict = {v: k for k, v in encoder_dict.items()}

    if len(encoder_dict) != len(decoder_dict):
        msg = f'There are duplicate key/values in the {classes_file_path}'
        logger.fatal(msg)
        raise Exception(msg)

    logger.info('getting "n/a" class code')
    try:
        dummy_value = encoder_dict['n/a']
    except Exception as ex:
        logger.error("Cannot get dummy value for class 'n/a'")
        logger.fatal(str(ex))
        raise KeyError
    logger.info(f'"n/a" class code: {dummy_value}')

    # df['scalar'] = df.tag_name.map(PRIORITY_TAG_SCALERS).fillna(1.0)

    if not os.path.exists(annotations_file_path):
        logger.warning(
            f'annotation file "{annotations_file_path}", does not exists')
        _ann = [np.array([])]
    else:
        _ann = np.loadtxt(annotations_file_path)
        logger.info(f"{_ann.shape[0]} annotation bas benn read")

    # _boxes = df[['x', 'y', 'width', 'height', 'scalar']].values
    _boxes_df = df[['x', 'y', 'width', 'height',
                    'displayed', 'is_hidden', 'tag_name', 'element_id']]

    labels = []
    i = 0

    for bb in tqdm(_ann, desc='Assign labels'):
        c, x, y, w, h = bb

        best_iou = 0.0001  # threshold to filter bad overlaps
        best_idx = -1       # fake value
        best_tag = 'n/a',
        best_rect = (0, 0, 0, 0)
        best_yolo = (0, 0, 0, 0)
        best_label = encoder_dict['n/a']

        for idx, r in _boxes_df.iterrows():

            #             if r.is_hidden or not r.displayed:  # Important: we must skip hidden and invisible nodes
            #                 continue

            iou = iou_xywh(from_yolo(x, y, w, h, img_width,
                           img_height), (r.x, r.y, r.width, r.height))

            if iou >= best_iou:  # We have to use >=, because the next tag might be more important
                best_idx, best_iou, best_tag, best_rect, best_yolo, best_label = (  # noqa
                    idx, iou, r.tag_name, (r.x, r.y, r.width, r.height), (x, y, w, h), c)  # noqa

        if best_idx == -1:  # make sure it is not a fake value
            logger.warning(
                f'LABEL IS NOT ASSIGNED: {annotations_file_path} {(x, y, w, h)}')
            continue

        labels.append({'idx': best_idx,
                       'label': float(best_label),
                       'annotation_line_no': i,
                       'iou': best_iou,
                       'tag': best_tag,
                       'label_text': decoder_dict[int(best_label)],
                       # 'best_rect': best_rect,
                       # 'best_yolo': best_yolo
                       })
        i += 1

    if len(labels) != 0:
        labels_df = pd.DataFrame(data=labels)
        if verbose:
            display(labels_df)

        labels_df.index = labels_df.idx
        df = df.merge(labels_df, how='left', left_index=True, right_index=True)
        df.label = df.label.fillna(dummy_value).astype(int)
        df.iou = df.iou.fillna(0.0)
        df.label_text = df.label_text.fillna('n/a')
    else:
        df['label'] = int(dummy_value)
        df['label_text'] = 'n/a'
        df['iou'] = 0.0

    # df.drop(columns=['iou', 'idx'], inplace=True)  # drop auxiliary columns

    return df
