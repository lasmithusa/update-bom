def get_deleted_idx(master_bom_df, new_bom_df, node_id='Node ID'):
    return ~master_bom_df.reset_index()[node_id].isin(new_bom_df.reset_index()[node_id]).values


def get_added_idx(master_bom_df, new_bom_df, node_id='Node ID'):
    return ~new_bom_df.reset_index()[node_id].isin(master_bom_df.reset_index()[node_id]).values


def get_comparison_columns(master_bom_df, new_bom_df):
    return [master_bom_column for master_bom_column in master_bom_df.columns if master_bom_column in new_bom_df.columns]


def get_support_columns(master_bom_df, new_bom_df):
    return [master_bom_column for master_bom_column in master_bom_df.columns if not master_bom_column in new_bom_df.columns]


def get_deleted_nodes(master_bom_df, new_bom_df, node_id='Node ID'):
    """Check master DF for nodes NOT in the new DF (nodes deleted in the new BOM)"""

    return master_bom_df[get_deleted_idx(master_bom_df, new_bom_df, node_id=node_id)].reset_index()[node_id].to_list()


def get_added_nodes(master_bom_df, new_bom_df, node_id='Node ID'):
    """Check new BOM DF for nodes NOT in the master DF (nodes added to the new BOM)"""

    return new_bom_df[get_added_idx(master_bom_df, new_bom_df, node_id=node_id)].reset_index()[node_id].to_list()


def get_added_columns_idx(master_bom_df, new_bom_df):
    return [new_bom_column if not new_bom_column in master_bom_df.columns else False for new_bom_column in new_bom_df.columns]


def get_added_columns(master_bom_df, new_bom_df):
    return [new_bom_column for new_bom_column in new_bom_df.columns if not new_bom_column in master_bom_df.columns]


def get_updated_elements(master_bom_df, new_bom_df, compare_columns=[None], deleted_idx=[None],
                    added_idx=[None], node_id='Node ID', order_only=False, order_id='Order'):
    if not any(compare_columns):
        compare_columns = get_comparison_columns(master_bom_df, new_bom_df)

    if not any(deleted_idx):
        deleted_idx = get_deleted_idx(master_bom_df, new_bom_df, node_id=node_id)

    if not any(added_idx):
        added_idx = get_added_idx(master_bom_df, new_bom_df, node_id=node_id)
    
    if order_only == False:
        drop = []
    elif order_only == None:
        drop = order_id
    else:
        drop = compare_columns

    master_bom_df_subset = master_bom_df.loc[~deleted_idx, compare_columns].reset_index().set_index(node_id).drop(columns=drop).fillna('')
    new_bom_df_subset = new_bom_df.loc[~added_idx, compare_columns].reset_index().set_index(node_id).drop(columns=drop).fillna('')
        
    return ~master_bom_df_subset.eq(new_bom_df_subset)


def get_updated_idx(master_bom_df, new_bom_df, compare_columns=[None], deleted_idx=[None],
                        added_idx=[None], node_id='Node ID', order_only=False, order_id='Order'):

    return get_updated_elements(master_bom_df, new_bom_df, compare_columns=compare_columns, deleted_idx=deleted_idx,
                    added_idx=added_idx, node_id=node_id, order_only=order_only, order_id=order_id).apply(any, axis=1)


def get_updated_nodes(master_bom_df, new_bom_df, compare_columns=[None], deleted_idx=[None],
                    added_idx=[None], node_id='Node ID', order_only=False, order_id='Order'):

    if not any(deleted_idx):
        deleted_idx = get_deleted_idx(master_bom_df, new_bom_df, node_id=node_id)
    
    updated_idx = get_updated_idx(master_bom_df, new_bom_df, compare_columns=compare_columns,
        deleted_idx=deleted_idx, added_idx=added_idx, node_id=node_id, order_only=order_only, order_id=order_id)

    return updated_idx[updated_idx].index.values


def get_reordered_idx(master_bom_df, new_bom_df, compare_columns=[None], deleted_idx=[None],
                                    added_idx=[None], node_id='Node ID', order_id='Order'):
    
    return get_updated_elements(master_bom_df=master_bom_df, new_bom_df=new_bom_df, compare_columns=compare_columns,
        deleted_idx=deleted_idx, added_idx=added_idx, node_id=node_id, order_only=True, order_id=order_id)[order_id].values


def get_reordered_nodes(master_bom_df, new_bom_df, compare_columns=[None], deleted_idx=[None],
                                        added_idx=[None], node_id='Node ID', order_id='Order'):

    if not any(deleted_idx):
        deleted_idx = get_deleted_idx(master_bom_df, new_bom_df, node_id=node_id)

    reordered_idx = get_reordered_idx(master_bom_df, new_bom_df, compare_columns=[None],
                deleted_idx=[None], added_idx=[None], node_id=node_id, order_id=order_id)

    return master_bom_df[~deleted_idx][reordered_idx].reset_index()[node_id].to_list()
