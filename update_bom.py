import argparse
from pandas import ExcelWriter
from bom_helper import read_xlsx_bom, add_node_ids, merge_support_columns
from id_nodes import id_nodes
from id_changes import get_deleted_nodes, get_added_nodes, get_reordered_nodes, get_updated_nodes, get_added_columns, get_updated_elements
from format_xlsx import highlight_added_columns, highlight_changes, generate_key_sheet, get_max_column_widths, set_sheets_column_widths, highlight_updated_elements
from os.path import basename, dirname, join

# setup argument parser
description = """BOM Management Tool for generating updated BOM sheets:
                merges supporting columns from the master BOM to the new BOM;
                indicates which BOM nodes were added, reordered, and deleted;
                and indicates which BOM elements / properties were updated."""

parser = argparse.ArgumentParser(description=description)
parser.add_argument("--master", type=str, help="Relative path to the master BOM workbook")
parser.add_argument("--new", type=str, help="Relative path to the new BOM workbook")
parser.add_argument("--outputname", default=None, type=str, help="Name of the output updated BOM (default: \"updated_\" pre-pended to the new BOM workbook name)")
parser.add_argument("--outputpath", default=None, type=str, help="Relative path to the output updated BOM (default: same as new BOM workbook path)")

# parse passed arguments
args = parser.parse_args()

master_bom_path = args.master
new_bom_path = args.new
updated_bom_name = args.outputname
updated_bom_dir_path = args.outputpath

if updated_bom_name == None:
    updated_bom_name = 'updated_{}'.format(basename(new_bom_path))

if updated_bom_dir_path == None:
    updated_bom_dir_path = dirname(new_bom_path)

updated_bom_path = join(updated_bom_dir_path, updated_bom_name)

# import BOMs
master_bom_df = read_xlsx_bom(master_bom_path)
new_bom_df = read_xlsx_bom(new_bom_path)

# add node IDs
master_bom_df = add_node_ids(master_bom_df)
new_bom_df = add_node_ids(new_bom_df)

# identify modified nodes
deleted_nodes = get_deleted_nodes(master_bom_df, new_bom_df)
added_nodes = get_added_nodes(master_bom_df, new_bom_df)
reordered_nodes = get_reordered_nodes(master_bom_df, new_bom_df)
updated_nodes = get_updated_nodes(master_bom_df, new_bom_df, order_only=None)

# identify added columns
added_columns = get_added_columns(master_bom_df, new_bom_df)

# identify updated elements
updated_elements = get_updated_elements(master_bom_df, new_bom_df, order_only=None)

# generate updated BOM
updated_bom_df = merge_support_columns(master_bom_df, new_bom_df)

# create XLSX writer object
writer = ExcelWriter(updated_bom_path, engine ='xlsxwriter')

# write DFs to sheet
updated_bom_df.to_excel(writer, sheet_name ='Updated BOM', index=False)
master_bom_df.loc[(slice(None), deleted_nodes), :].to_excel(writer, sheet_name ='Removed Nodes', index=False)
new_bom_df.loc[(slice(None), added_nodes), :].to_excel(writer, sheet_name ='Added Nodes', index=False)
master_bom_df.loc[(slice(None), updated_nodes), :].to_excel(writer, sheet_name ='Updated Nodes', index=False)
master_bom_df.loc[(slice(None), reordered_nodes), :].to_excel(writer, sheet_name ='Reordered Nodes', index=False)

# create workbook object for XLSX formatting control
workbook = writer.book

# set formats
added_column_header_format = workbook.add_format({'bg_color': '#00B0F0', 'bold': True, 'border': 1, 'align': 'center_across', 'valign': 'top'})
added_node_format = workbook.add_format({'bg_color': '#00B0F0'})
reordered_node_format = workbook.add_format({'bg_color': '#92D050'})
updated_element_format = workbook.add_format({'bg_color': '#FFFF00'})

# grab worksheet to for format editing
updated_bom_sheet = workbook.get_worksheet_by_name('Updated BOM')
updated_nodes_sheet = workbook.get_worksheet_by_name('Updated Nodes')

# highlight added columns
highlight_added_columns(updated_bom_df, updated_bom_sheet, added_columns, added_column_header_format)

# highlight changes
highlight_changes(updated_bom_df, updated_bom_sheet, added_nodes, reordered_nodes, updated_nodes,
                updated_elements, added_node_format, reordered_node_format, updated_element_format)

highlight_updated_elements(master_bom_df.loc[(slice(None), updated_nodes), :], updated_nodes_sheet, updated_nodes, updated_elements, updated_element_format)

# get max columns widths and set sheet column widths
updated_added_max_column_widths = get_max_column_widths(updated_bom_df, buffer=2)
other_max_column_widths = get_max_column_widths(master_bom_df.loc[(slice(None), updated_nodes), :], buffer=2)

updated_added_sheets = [worksheet for worksheet in workbook.worksheets() if (worksheet.name == 'Updated BOM' or worksheet.name == 'Added Nodes')]
other_sheets = [worksheet for worksheet in workbook.worksheets() if not worksheet in updated_added_sheets]

set_sheets_column_widths(updated_added_sheets, updated_added_max_column_widths)
set_sheets_column_widths(other_sheets, other_max_column_widths)

# write key sheet
generate_key_sheet(workbook, added_node_format, reordered_node_format, updated_element_format)

# save workbook
writer.save()
