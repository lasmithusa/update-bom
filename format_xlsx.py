def highlight_added_columns(updated_bom_df, updated_bom_sheet, added_columns, added_column_header_format):

    for column_name in added_columns:
        updated_bom_sheet.write(0, updated_bom_df.columns.get_loc(column_name), column_name, added_column_header_format)


def highlight_changes(updated_bom_df, updated_bom_sheet, added_nodes, reordered_nodes, updated_nodes,
                    updated_elements, added_node_format, reordered_node_format, updated_element_format):
    
    for node_position, node_name in enumerate(updated_bom_df.index.get_level_values('Node ID')):
        if node_name in added_nodes:
            updated_bom_sheet.write(node_position + 1, updated_bom_df.columns.get_loc('Level'), updated_bom_df.loc[(slice(None), node_name), 'Level'].values[0], added_node_format)
            updated_bom_sheet.write_string(node_position + 1, updated_bom_df.columns.get_loc('File Name'), updated_bom_df.loc[(slice(None), node_name), 'File Name'].values[0], added_node_format)

        if node_name in reordered_nodes:
            updated_bom_sheet.write(node_position + 1, updated_bom_df.columns.get_loc('Level'), updated_bom_df.loc[(slice(None), node_name), 'Level'].values[0], reordered_node_format)
            updated_bom_sheet.write_string(node_position + 1, updated_bom_df.columns.get_loc('File Name'), updated_bom_df.loc[(slice(None), node_name), 'File Name'].values[0], reordered_node_format)

        if node_name in updated_nodes:
            for updated_column in updated_elements.loc[node_name, updated_elements.loc[node_name]].index.values:
                updated_bom_sheet.write(node_position + 1, updated_bom_df.columns.get_loc(updated_column), updated_bom_df.loc[(slice(None), node_name), updated_column].values[0], updated_element_format)


def highlight_updated_elements(updated_nodes_df, updated_nodes_sheet, updated_nodes, updated_elements, updated_element_format):
    for node_position, node_name in enumerate(updated_nodes_df.index.get_level_values('Node ID')):
        if node_name in updated_nodes:
            for updated_column in updated_elements.loc[node_name, updated_elements.loc[node_name]].index.values:
                updated_nodes_sheet.write(node_position + 1, updated_nodes_df.columns.get_loc(updated_column), updated_nodes_df.loc[(slice(None), node_name), updated_column].values[0], updated_element_format)


def generate_key_sheet(xlsx_workbook, added_node_format, reordered_node_format, updated_element_format,
                    added_node_text = 'Added nodes or columns', reordered_node_text = 'Re-ordered nodes',
                    updated_element_text = 'Updated nodes', key_sheet_name='Color Key', key_width=24):

    key_width = max(len(added_node_text), len(reordered_node_text), len(updated_element_text))

    xlsx_workbook.add_worksheet(key_sheet_name)

    key_sheet = xlsx_workbook.get_worksheet_by_name(key_sheet_name)
    key_sheet.write(0, 0, reordered_node_text, reordered_node_format)
    key_sheet.write(1, 0, added_node_text, added_node_format)
    key_sheet.write(2, 0, updated_element_text, updated_element_format)
    key_sheet.set_column(0, 0, key_width)


def set_sheet_column_widths(xlsx_sheet, widths=[5, 60, 60, 60, 15, 60, 10, 10, 15]):
    for column_num, width in enumerate(widths):
        xlsx_sheet.set_column(column_num, column_num, width)


def set_sheets_column_widths(xlsx_sheets, widths):
    for xlsx_sheet in xlsx_sheets:
        set_sheet_column_widths(xlsx_sheet, widths)


def get_max_column_widths(df, buffer=0):
    max_element_widths = df.applymap(str).applymap(len).apply(max).values
    column_name_widths = [len(column_name) for column_name in df.columns.values]
    return [max(max_element_width, column_width) + buffer for max_element_width, column_width in zip(max_element_widths, column_name_widths)]
