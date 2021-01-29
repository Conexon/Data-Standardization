#import python from geoprocessing in arcmap
#insert the path to your wo staking grid for sortFeat
import arcpy

sortFeat  = r'Z:\Petit Jean\staking_grid\s5.shp' 
sortField = 'pagename' 
idField   = 'PDFpage' 
rec=0

def autoIncrement():
    global rec
    pStart    = 1 
    pInterval = 1 
    if (rec == 0): 
        rec = pStart 
    else: 
        rec += pInterval 
    return rec

rows = arcpy.UpdateCursor(sortFeat, "", "", "", sortField + " A")

for row in rows:
    row.setValue(idField, autoIncrement())
    rows.updateRow(row)

del row, rows