from id_changes import get_support_columns, get_deleted_nodes

def merge_support_columns(master_bom_df, new_bom_df, support_columns=None, deleted_nodes=None, node_id='Node ID'):
    if support_columns == None:
        support_columns = get_support_columns(master_bom_df, new_bom_df)

    if deleted_nodes == None:
        deleted_nodes = get_deleted_nodes(master_bom_df, new_bom_df, node_id=node_id)

    return new_bom_df.merge(master_bom_df.loc[~deleted_nodes, support_columns], on=node_id', how='outer')