def get_comparison_columns(master_bom_df, new_bom_df):
    return [master_bom_column for master_bom_column in master_bom_df.columns if master_bom_column in new_bom_df.columns]


def get_support_columns(master_bom_df, new_bom_df):
    return [master_bom_column for master_bom_column in master_bom_df.columns if not master_bom_column in new_bom_df.columns]


def get_deleted_nodes(master_bom_df, new_bom_df, node_id='Node ID'):
    """Check master DF for nodes NOT in the new DF (nodes deleted in the new BOM)"""

    return ~master_bom_df.reset_index()[node_id].isin(new_bom_df.reset_index()[node_id]).values


def get_added_nodes(master_bom_df, new_bom_df, node_id='Node ID'):
    return ~new_bom_df.reset_index()[node_id].isin(master_bom_df.reset_index()[node_id]).values


def get_new_columns(master_bom_df, new_bom_df):
    return [new_bom_column for new_bom_column in new_bom_df.columns if not new_bom_column in master_bom_df.columns]


def get_updated_elements(master_bom_df, new_bom_df, compare_columns=None, deleted_nodes=None,
                    added_nodes=None, node_id='Node ID', order_only=False, order_id='Order'):
    if compare_columns == None:
        compare_columns = get_comparison_columns(master_bom_df, new_bom_df)

    if deleted_nodes == None:
        deleted_nodes = get_deleted_nodes(master_bom_df, new_bom_df, node_id=node_id)

    if added_nodes == None:
        added_nodes = get_added_nodes(master_bom_df, new_bom_df, node_id=node_id)
    
    if order_only == False:
        drop = []
    elif order_only == None:
        drop = order_id
    else:
        drop = compare_columns

    master_bom_df_subset = master_bom_df.loc[~deleted_nodes, compare_columns].reset_index().set_index(node_id).drop(columns=drop)
    new_bom_df_subset = new_bom_df.loc[~added_nodes, compare_columns].reset_index().set_index(node_id).drop(columns=drop)
        
    return ~master_bom_df_subset.eq(new_bom_df_subset)