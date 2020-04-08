from pandas import read_excel
from id_changes import get_support_columns, get_deleted_idx
from id_nodes import id_nodes


def read_xlsx_bom(bom_path, order_id='Order'):
    bom_df = read_excel(bom_path)
    bom_df.index.set_names(order_id, inplace=True)
    return bom_df


def add_node_ids(bom_df, node_id='Node ID'):
    bom_df[node_id] = id_nodes(bom_df)
    return bom_df.set_index(node_id, append=True)


def merge_support_columns(master_bom_df, new_bom_df, support_columns=[None], deleted_idx=[None], node_id='Node ID'):
    if not any(support_columns):
        support_columns = get_support_columns(master_bom_df, new_bom_df)

    if not any(deleted_idx):
        deleted_idx = get_deleted_idx(master_bom_df, new_bom_df, node_id=node_id)

    updated_bom_df = new_bom_df.merge(master_bom_df.loc[~deleted_idx, support_columns], on=node_id, how='outer').reset_index().set_index('Node ID', append=True)
    updated_bom_df.index.set_names(['Order', 'Node ID'], inplace=True)
    return updated_bom_df