# Projections Projections everywhere

![Alt text](images/projections.png?raw=true "Projections Projections everywhere")

## Purpose

Option for more efficient coordinate reprojection for geospatial data not in WGS84.

Removes dependency on 'serial feature conversion using a webservice' being error prone and causing overhead and delay.

## Prerequisites

Recent `Python3` with `Pandas` and `odfpy`.

```
python3 -m pip install --upgrade pip
python3 -m pip install pandas odfpy
```

## Steps

In this example I start with Dutch RD-coördinaatpunten data from https://www.nsgi.nl/documents/1888506/3754578/20220111+Lijst+actuele+kernnetpunten+voor+RDinfo.ods/ae6fecb4-e145-8d93-8a91-fc578dd18d52?t=1641991881508
This file comes in OpenDocument Spreadsheet (ods) file format [1]. More common is probably getting csv or Esri Shapefile as input.

1.
Create csv from ods file

```
python3 ods2csv.py
```

Result is file `input.csv`.

2.
Transform RD EPSG:28992 to UTM Zone 32N EPSG:23032 and WGS84 EPSG:4326

```
python3 ogr_proj.py
```

Result is file `output.csv`.

NOTE: Very important is not to do 'serial reprojections'!! E.g. 28992 to 23032 to 4326. Determine original Coordinate Reference System (CRS)for source, in this case that is RD or EPSG:28992, ETRS89 is derived CRS here (a nice read is on this topic is 'De geodetische referentiestelsels van Nederland - Geodetic reference frames in the Netherlands' [5]). Use the source CRS every time for conversion to another system. E.g. 28992 to 23032, 28992 to 4326 etc. Also check how many deciamls make sense in the resulting output.

3.
TODO: Describe role of vrt file

4.
Could do further processing like convert to geojson, ...

## Check result file

Go to https://geojson.io/ [2]

Click [ Open ] and select `output.csv`. Will load the file assuming `lat` and `lon` to contain WGS84 coordinates. Can export to geojson and more.

![Alt text](images/geojson.io.1.png?raw=true "geojson.io")

![Alt text](images/geojson.io.2.png?raw=true "kernnetpunten rijksdriehoekmeting")

## Links

[1]
https://www.nsgi.nl/geodetische-infrastructuur/referentiestelsels/rdinfo

[2]
https://geojson.io/

[3]
https://geojson.tools/

[4]
https://geojsonlint.com/

[5]
https://ncgeo.nl/downloads/43Referentie.pdf