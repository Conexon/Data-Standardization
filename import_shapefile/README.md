# Importing data into pgAdmin

When we recieve new client data, typically the data is in a geodatabase that we cannot directly import into our pgAdmin database, so the first step is to save the data to your local drive, unzip the gdb, and then open QGIS.

### Opening GDB in QGIS

* Under the "Layer" tab at the top of QGIS, select "Add Layer", then "Add Vector Layer..."
* Set the source type as "Directory", leave encoding as "Automatic", set Type as "OpenFileGDB", and set the vector dateset to the .gdb folder you wish to open.

<img src="https://github.com/Conexon/Data-Standardization/blob/master/import_shapefile/qgis_gdb_import.PNG" width="750" height="200">

* Select which layers you want to bring in from the GDB and hit okay on any transformation pop-ups.
* On the bottom right of QGIS, there should now be a number after "EPSG:". Note this number, as it is the SRID projection number of your client.

### Save layers as shapefiles in QGIS
* Right click on the layer, "Export", "Save Feature as..."
* Check that the Format is "ESRI Shapefile".
* Select the name and location of the shapefile.
* Check that the CRS value is the same EPSG number as in the bottom right of QGIS.

## Import Shapefiles into pgAdmin
There are 3 ways to import shapefiles into pgAdmin. Each are detailed below.

### Command Line
This method allows for shapefiles to be imported from your local drive to pgAdmin through the Windows Command Terminal.

Script with instructions on how to run can be found [**here**](https://github.com/Conexon/Data-Standardization/blob/master/import_shapefile/shapefile_import_command).

### QGIS Connection
Connecting pgAdmin directly to QGIS is the most efficient way (in my opinion) of importing shapefiles to pgAdmin. Having this connection is nice because it allows you to view the spatial attributes of your database and make changes to the database directly through QGIS.

Instruction of how to connect pgAdmin to your QGIS can be found here.

Once the connection is made. All you need to do is to drag the new shapefiles into the schema of you choice.

### PostGIS Shapefile Importer/Exporter
