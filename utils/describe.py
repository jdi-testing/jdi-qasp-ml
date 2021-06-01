import pandas as pd
from .common import build_tree_dict
from .common import build_elements_dict
from .features_builder import build_siblings_dict
from IPython.display import display, HTML
# from .config import logger


def describe_node(df: pd.DataFrame,
                  element_id: str,
                  tree_dict: dict = None,
                  elements_dict: dict = None,
                  siblings_dict: dict = None
                  ):
    if tree_dict is None:
        # logger.info('Build tree_dict')
        tree_dict = build_tree_dict(df=df)

    if elements_dict is None:
        # logger.info('Build elements_dict')
        elements_dict = build_elements_dict(df=df)

    if siblings_dict is None:
        # logger.info('Build Siblings dict')
        siblings_dict = build_siblings_dict(df=df)

    display(HTML(f'Describe node: <b>{element_id}<b>'))

    # parents
    display(HTML('<b>Parents:</b>'))
    p = element_id
    parents_list = []
    while p is not None:
        n = elements_dict[p]
        n['element_id'] = p
        parents_list.append(n)
        p = tree_dict[p]

    display(pd.DataFrame(parents_list))

    # siblings
    p = tree_dict[element_id]
    if p is None:
        display(HTML('<b>No siblins</b>'))
    else:
        display(HTML('<b>Siblings:</b>'))
    siblings = siblings_dict[p]
    siblings_list = [elements_dict[k] for k in siblings.keys()]
    display(pd.DataFrame(siblings_list))
