import numba
import pandas as pd
# import numba
from .config import logger
from .common import iou_xywh


FIELDS_SET = set(['x', 'y', 'width', 'height', 'displayed', 'tag_name'])


@numba.jit
def check_is_inside(parent_rect, child_rect):
    """
        rect: (x,y,w,h),
        returns (fully_inside, patrually_inside, intersectio_over_union)
    """

    px1, py1, pw, ph = parent_rect
    px2, py2 = px1 + pw, py1 + ph

    print('Parent', px1, py1, px2, py2, (pw, ph))

    cx1, cy1, cw, ch = child_rect
    cx2, cy2 = cx1 + cw, cy1 + ch
    print('Child', cx1, cy1, cx2, cy2, (cw, ch))

    if cx2 <= px1:
        return (0.0, 0.0, 0.0)
    if cx1 >= px2:
        return (0.0, 0.0, 0.0)
    if cy1 >= py2:
        return (0.0, 0.0, 0.0)
    if cy2 <= px1:
        return (0.0, 0.0, 0.0)

    cx1_inside = True if (cx1 >= px1) and (cx1 <= px2) else False
    cx2_inside = True if (cx2 >= px1) and (cx2 <= px2) else False

    cy1_inside = True if (cy1 >= py1) and (cy1 <= py2) else False
    cy2_inside = True if (cy2 >= py1) and (cy2 <= py2) else False

    # calculate intersection size
    ix1, ix2, iy1, iy2 = max(cx1, px1), min(cx2, px2), max(cy1, py1), min(cy2, py2)
    iw, ih = ix2 - ix1, iy2 - iy1
    print('Intersection:', ix1, iy1, ix2, iy2, iw, ih)

    if (iw > 0.0) and (ih > 0.0) and (pw > 0.0) and (ph > 0.0) and (cw > 0.0) and (ch > 0.0):
        si = iw * ih  # intersection's square
        iou = si / (pw * ph + cw * ch - si)  # ratio: Intersection over Union (IoU)
    else:
        iou = 0.0

    if cx1_inside and cx2_inside and cy1_inside and cy2_inside:
        return (1.0, 0.0, iou)
    else:
        return (0.0, 1.0, iou)


def build_is_hidden(df: pd.DataFrame) -> pd.DataFrame:
    """
        Checks, whether the control is hidden.
        df have to contain fileds: ['x', 'y', 'width', 'height', 'displayed', 'tag_name']
    """
    if len(set(df.columns).intersection(FIELDS_SET)) != len(FIELDS_SET):
        raise Exception(f'No required fields: {FIELDS_SET}')

    tree_dict = {
        r.element_id: None if r.element_id == r.parent_id else r.parent_id
        for _, r in df[['element_id', 'parent_id']].iterrows()
    }

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
            parent_properties = elements_dict[parent]
            if parent_properties['d']:  # skip not displayed parents
                iou = iou_xywh(box, elements_dict[parent]['box'])

                # if control is out of parent's rectangle
                if iou == 0.0:
                    result = True
                    break

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
