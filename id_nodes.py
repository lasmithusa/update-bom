import pandas as pd

def id_immediate_parent(df_child_row, df):
    immediate_parent_level = -1
    immediate_parent_index = -1
    immediate_parent_file_name = ''

    if not df_child_row['Level'] == 0:
        # get parent level
        immediate_parent_level = df_child_row['Level'] - 1

        # get parent index
        immediate_parent_index = df['Level'].iloc[:df_child_row.name].eq(immediate_parent_level).sort_index(ascending=False).idxmax()

        # get parent file name
        immediate_parent_file_name = df.at[immediate_parent_index, 'File Name'].strip()

    return [df_child_row.name, immediate_parent_index, immediate_parent_level, immediate_parent_file_name]

def generate_immediate_parent_id_df(df):
    immediate_parent_id_df = df.apply(func=id_immediate_parent, axis=1, result_type='expand', args=(df, ))
    immediate_parent_id_df.columns = ['Order', 'Immediate Parent Index', 'Immediate Parent Level', 'Immediate Parent File Name']
    return immediate_parent_id_df.set_index('Order')

def crawl_immediate_parents(child_row, immediate_parent_id_df):
    if child_row['Immediate Parent Level'] == -1:
        return [], [], []
    else:
        parent_row = immediate_parent_id_df.loc[child_row['Immediate Parent Index']]

        parent_indices, parent_levels, parent_file_names = crawl_immediate_parents(parent_row, immediate_parent_id_df)

        parent_indices.extend([child_row['Immediate Parent Index']])
        parent_levels.extend([child_row['Immediate Parent Level']])
        parent_file_names.extend([child_row['Immediate Parent File Name']])
        
        return parent_indices, parent_levels, parent_file_names

def generate_all_parent_id_df(df):
    immediate_parent_id_df = generate_immediate_parent_id_df(df)
    all_parent_id_df = immediate_parent_id_df.apply(crawl_immediate_parents, axis=1, result_type='expand', args=(immediate_parent_id_df, ))
    all_parent_id_df.columns = ['Parent Indices', 'Parent Levels', 'Parent File Names']
    
    return all_parent_id_df

def id_parents(df):
    return generate_all_parent_id_df(df)['Parent File Names'].str.join('->')

def id_nodes(df):
    return id_parents(df).str.cat(master_df['File Name'].str.strip(), sep="->")

if __name__ == '__main__':
    master_path = r"..\Master-0015442-FS-8100-BOM-20200326.xlsx"
    compared_path = r"..\0015442-FS-8100-BOM-20200326.xlsx"
    
    master_df = pd.read_excel(master_path)
    compared_df = pd.read_excel(compared_path)

    master_df.index.set_names('Order', inplace=True)
    compared_df.index.set_names('Order', inplace=True)

    master_df['Node ID'] = id_nodes(master_df)
    compared_df['Node ID'] = id_nodes(compared_df)

    