import pandas as pd
import numpy as np
from MUI_model.utils.config import logger
from scipy.sparse.csr import csr_matrix
from scipy.sparse import hstack


from MUI_model.utils.features_builder import build_attributes_feature
from MUI_model.utils.features_builder import build_class_feature
from MUI_model.utils.features_builder import build_role_feature
from MUI_model.utils.features_builder import build_tag_name_feature
from MUI_model.utils.features_builder import build_type_feature
from MUI_model.utils.features_builder import build_children_tags
from MUI_model.utils.features_builder import build_followers_tags


COLS = ['element_id', 'tag_name', 'attributes', 'displayed', 'is_hidden']

TARGET_PARENT_COLUMNS = ['parent_id', 'tag_name_parent',
                         'attributes_parent', 'displayed_parent', 'is_hidden_parent']

TARGET_UP_SIBLING_COLUMNS = [
    'upper_sibling', 'tag_name_upsib', 'attributes_upsib', 'displayed_upsib', 'is_hidden_upsib']

TARGET_DN_SIBLING_COLUMNS = [
    'lower_sibling', 'tag_name_dnsib', 'attributes_dnsib', 'displayed_dnsib', 'is_hidden_dnsib']


def collect_dataset(df: pd.DataFrame) -> csr_matrix:
    df_parent = df[COLS].copy()
    df_parent.columns = TARGET_PARENT_COLUMNS

    upsib_df = df[COLS].copy()
    upsib_df.columns = TARGET_UP_SIBLING_COLUMNS

    dnsib_df = df[COLS].copy()
    dnsib_df.columns = TARGET_DN_SIBLING_COLUMNS

    dataset_df = df.merge(df_parent, on='parent_id', how='left')
    dataset_df = dataset_df.merge(upsib_df, on='upper_sibling', how='left')
    dataset_df = dataset_df.merge(dnsib_df, on='lower_sibling', how='left')

    y = df.label.values

    # tag_name
    tag_name_sm = build_tag_name_feature(dataset_df, colname='tag_name')
    parent_tag_name_sm = build_tag_name_feature(dataset_df, colname='tag_name_parent')
    upsib_tag_name_sm = build_tag_name_feature(dataset_df, colname='tag_name_upsib')
    dnsib_tag_name_sm = build_tag_name_feature(dataset_df, colname='tag_name_dnsib')
    logger.info(f'tag_name: {tag_name_sm.shape}')

    # attributes
    attributes_sm = csr_matrix(build_attributes_feature(df=dataset_df, colname='attributes_parent').values)
    parent_attributes_sm = csr_matrix(build_attributes_feature(df=dataset_df, colname='attributes_parent').values)
    upsib_attributes_sm = csr_matrix(build_attributes_feature(df=dataset_df, colname='attributes_upsib').values)
    dnsib_attributes_sm = csr_matrix(build_attributes_feature(df=dataset_df, colname='attributes_dnsib').values)
    logger.info(f'attributes_sm: {attributes_sm.shape}')

    # class
    class_sm = build_class_feature(dataset_df, colname='attributes')
    parent_class_sm = build_class_feature(dataset_df, colname='attributes_parent')
    upsib_class_sm = build_class_feature(dataset_df, colname='attributes_upsib')
    dnsib_class_sm = build_class_feature(dataset_df, colname='attributes_dnsib')
    logger.info(f'class_sm: {class_sm.shape}')

    # type
    type_sm = build_type_feature(dataset_df, colname='attributes')
    parent_type_sm = build_type_feature(dataset_df, colname='attributes_parent')
    upsib_type_sm = build_type_feature(dataset_df, colname='attributes_upsib')
    dnsib_type_sm = build_type_feature(dataset_df, colname='attributes_dnsib')
    logger.info(f'type_sm: {type_sm.shape}')

    # role
    role_sm = build_role_feature(dataset_df, colname='attributes')
    parent_role_sm = build_role_feature(dataset_df, colname='attributes_parent')
    upsib_role_sm = build_role_feature(dataset_df, colname='attributes_upsib')
    dnsib_role_sm = build_role_feature(dataset_df, colname='attributes_dnsib')
    logger.info(f'role_sm: {role_sm.shape}')

    # children & followers tags
    child_tags_sm = build_children_tags(dataset_df, colname='children_tags')
    foll_tags_sm = build_followers_tags(dataset_df, colname='followers_tags')

    X = np.array(hstack([
        attributes_sm,
        parent_attributes_sm,
        upsib_attributes_sm,
        dnsib_attributes_sm,
        class_sm,
        parent_class_sm,
        upsib_class_sm,
        dnsib_class_sm,
        tag_name_sm,
        parent_tag_name_sm,
        upsib_tag_name_sm,
        dnsib_tag_name_sm,
        type_sm,
        parent_type_sm,
        upsib_type_sm,
        dnsib_type_sm,
        role_sm,
        parent_role_sm,
        upsib_role_sm,
        dnsib_role_sm,
        child_tags_sm,
        foll_tags_sm,
        dataset_df.num_followers.fillna(False).astype(int).values.reshape(-1, 1),
        dataset_df.is_leaf.fillna(False).astype(int).values.reshape(-1, 1),
        dataset_df.num_leafs.fillna(False).astype(int).values.reshape(-1, 1),
        dataset_df.num_children.fillna(False).astype(int).values.reshape(-1, 1),
        dataset_df.sum_children_widths.fillna(False).astype(int).values.reshape(-1, 1),
        dataset_df.sum_children_hights.fillna(False).astype(int).values.reshape(-1, 1),
        dataset_df.max_depth.astype(int).values.reshape(-1, 1),
        dataset_df.displayed.astype(int).values.reshape(-1, 1),
        dataset_df.displayed_parent.fillna(False).astype(int).values.reshape(-1, 1),
        dataset_df.displayed_upsib.fillna(False).astype(int).values.reshape(-1, 1),
        dataset_df.displayed_dnsib.fillna(False).astype(int).values.reshape(-1, 1),
        dataset_df.is_hidden.fillna(1.0).values.reshape(-1, 1),
        dataset_df.is_hidden_parent.fillna(1.0).values.reshape(-1, 1),
        dataset_df.is_hidden_upsib.fillna(1.0).values.reshape(-1, 1),
        dataset_df.is_hidden_dnsib.fillna(1.0).values.reshape(-1, 1)
    ]).todense())  # I hope we have enougth RAM

    logger.info(f'X: {X.shape}')
    return X.astype(np.float32), y
