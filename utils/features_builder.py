import pandas as pd
from .common import build_elements_dict  # noqa
from .common import build_tree_dict
from .hidden import build_is_hidden


def build_siblings_dict(df: pd.DataFrame):
    """
        returns dictionary of nodes which has children
        idx - is an index in the df dataframe

    """

    from collections import defaultdict

    siblings_dict = defaultdict(dict)

    for idx, r in df.iterrows():
        if (r.parent_id == r.element_id) or (r.parent_id is None):
            continue

        p = siblings_dict[r.parent_id]
        p[r.element_id] = idx

    return siblings_dict


def get_siblings(siblings_dict: dict, tree_dict: dict, index_dict: dict, element_id: str):
    """
        Returns a pair of siblings (before_sibling, after_sibling)
        for a specified element_id
    """
    parent = tree_dict[element_id]
    siblings = siblings_dict[parent]
    # print('e:', element_id, ', p:', parent, ', s:', siblings)

    idx = siblings.get(element_id)
    if idx is None:  # in the case the element is not found
        return (None, None)

    indices = siblings.values()
    # print(idx, indices)

    up_siblings = [v for v in indices if v < idx]
    dn_siblings = [v for v in indices if v > idx]
    if len(up_siblings) == 0:
        up = None
    else:
        up = max(up_siblings)
    if len(dn_siblings) == 0:
        dn = None
    else:
        dn = min(dn_siblings)

    return index_dict.get(up), index_dict.get(dn)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
        Enrich dataset with features.
        The df:pd.DataFrame must have columns: ['element_id', 'parent_id', 'x', 'y', 'width', 'height']
    """

    # build IS_HIDDEN feature
    build_is_hidden(df)

    siblings_dict = build_siblings_dict(df)
    index_dict = {idx: r.element_id for idx,
                  r in df.iterrows() if r.element_id != r.parent_id}

    # elements_dict = build_elements_dict(df)
    tree_dict = build_tree_dict(df)

    elements = df.element_id.values  # get siblings for each element

    siblings = [get_siblings(siblings_dict=siblings_dict,
                             tree_dict=tree_dict,
                             index_dict=index_dict,
                             element_id=e)
                for e in elements]

    df['upper_sibling'] = [s[0] for s in siblings]
    df['lower_sibling'] = [s[1] for s in siblings]
    df['siblings'] = siblings

    return df
