# update-bom
A Bill of Materials (BOM) Update Tool

updatebom CLI Tool – 
Tool Features:
1.	Merge manually added columns in the “master” BOM with the new BOM.
    1. These columns could be Lead Time, Cost, Notes, or any other details your team has added to the BOM sheet.
    2.  Column data is properly aligned regardless of whether the parts in the BOM have changed order.
2.	Highlight all changes to BOM node properties with yellow.	
    1.	BOM node properties include things like Description, Quantity, Status, etc…
3.	Highlight all added BOM nodes and columns with blue.
    1.	New data columns (Material, for example) will be highlighted blue.
4.	Highlight all re-ordered BOM nodes with green.
5.	List removed, added, updated, and reordered nodes in separate sheets within the workbook for reference.

Required inputs:
1.	Path to master BOM workbook (--master)
2.	Path to new BOM workbook (--new)

Optional inputs:
1.	Output updated BOM name (--outputname) – default: “updated_” pre-prended to the new BOM workbook name
2.	Output updated BOM path (--outputpath) – default: new BOM workbook path

A zip file containing an executable (entire folder must be added to system path), can be found here: https://drive.google.com/file/d/18ZVMWR4-5OGvh8fDc6wGk4Rm4j5NAeIu
