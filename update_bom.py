from id_changes import get_support_columns, get_deleted_idx

def merge_support_columns(master_bom_df, new_bom_df, support_columns=[None], deleted_idx=[None], node_id='Node ID'):
    if not any(support_columns):
        support_columns = get_support_columns(master_bom_df, new_bom_df)

    if not any(deleted_idx):
        deleted_idx = get_deleted_idx(master_bom_df, new_bom_df, node_id=node_id)

    return new_bom_df.merge(master_bom_df.loc[~deleted_idx, support_columns], on=node_id, how='outer')