# Importing data to pgAdmin

When we recieve new client data, typically the data is in a geodatabase that we cannot directly import into our pgAdmin database, so the first step is to save the data to your local drive, unzip the gdb, and then open QGIS.

### Opening GDB in QGIS

* Under the "Layer" tab at the top of QGIS, select "Add Layer", then "Add Vector Layer..."
* Set the source type as "Directory", leave encoding as "Automatic", set Type as "OpenFileGDB", and set the vector dateset to the .gdb folder you wish to open.
* Select which layers you want to bring in from the GDB and hit okay on any transformation pop-ups.
* On the bottom right of QGIS, there should now be a number after "EPSG:". Note this number, as it is the SRID projection number of your client.

### Save layers as shapefiles in QGIS
* Right click on the layer, "Export", "Save Feature as..."
* Check that the Format is "ESRI Shapefile".
* Select the name and location of the shapefile.
* Check that the CRS value is the same EPSG number as in the bottom right og QGIS.
