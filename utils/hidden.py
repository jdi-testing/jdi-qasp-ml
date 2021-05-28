import pandas as pd
# import numba
from .config import logger
from .common import iou_xywh


FIELDS_SET = set(['x', 'y', 'width', 'height', 'displayed', 'tag_name'])


def build_is_hidden(df: pd.DataFrame) -> pd.DataFrame:
    """
        Checks, whether the control is hidden.
        df have to contain fileds: ['x', 'y', 'width', 'height', 'displayed', 'tag_name']
    """
    if len(set(df.columns).intersection(FIELDS_SET)) != len(FIELDS_SET):
        raise Exception(f'No required fields: {FIELDS_SET}')

    tree_dict = {r.element_id: r.parent_id for idx, r in df.iterrows()}

    elements_dict = {r.element_id: {
        'box': (r.x, r.y, r.width, r.height),
        'd': r.displayed,
        't': r.tag_name
    } for _, r in df.iterrows()}

    # @numba.jit
    def is_hidden(child):
        result = False
        box = elements_dict[child]['box']
        parent = tree_dict[child]

        while tree_dict[parent] is not None:
            iou = iou_xywh(box, elements_dict[parent]['box'])

            # if control is out of parent's rectangle
            if iou == 0.0:
                result = True
                break

            # # if parent is not displayed
            # if elements_dict[parent]['d'] is False:
            #     result = True
            #     break

            parent = tree_dict[parent]
        return result

    logger.info('build field "is_hidden"')

    # @numba.jit
    def process_controls():
        # process only controls which are displayed
        # result_dict = {child: is_hidden(child) for child in tree_dict if tree_dict[child]['d'] is True}
        result_dict = {child: is_hidden(child) for child in tree_dict if tree_dict.get(child) is not None}
        return result_dict

    is_hidden_dict = process_controls()
    df['is_hidden'] = df.element_id.map(is_hidden_dict).fillna(False).astype(int)
    return df


logger.info('hidden module is loaded')
