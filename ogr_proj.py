from osgeo import ogr, osr
import csv

# Define the input and output file paths
input_file = 'data/input.vrt'
output_file = 'data/output.csv'

# Create a spatial reference for EPSG:28992 (RD New)
source_sr_28992 = osr.SpatialReference()
source_sr_28992.ImportFromEPSG(28992)

# Create a spatial reference for EPSG:23032 (UTM Zone 32N)
target_sr_23032 = osr.SpatialReference()
target_sr_23032.ImportFromEPSG(23032)

# Create a spatial reference for EPSG:4326 (WGS84)
target_sr_4326 = osr.SpatialReference()
target_sr_4326.ImportFromEPSG(4326)

# Create a coordinate transformation from source to target
transform_28992_23032 = osr.CoordinateTransformation(source_sr_28992, target_sr_23032)
transform_28992_4326 = osr.CoordinateTransformation(source_sr_28992, target_sr_4326)

# Open the input VRT file
input_dataset = ogr.Open(input_file)
input_layer = input_dataset.GetLayer()

# Get the field names from the input layer
field_names = [field.GetName() for field in input_layer.schema]

# Create the output CSV file and write the header
output_dataset = open(output_file, 'w', newline='')
csv_writer = csv.writer(output_dataset, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
csv_writer.writerow(field_names + ['x', 'y', 'lon', 'lat'])

# Iterate over features in the input layer
# use separate 'split' features for two instances of the input layer
# cannot 'reuse' feature for multipe transform operations, messes up result
# also cannot use module copy because feature is not supported for for deepcopy  
for feature_23032, feature_4326 in zip(input_layer, input_layer):
    # Get the attributes from the input feature
    # Use any of the feature_* here to get the field names
    attributes = [feature_23032.GetField(field_name) for field_name in field_names]

    # Get the geometry from the input feature
    geometry_28992_23032 = feature_23032.GetGeometryRef()
    geometry_28992_4326 = feature_4326.GetGeometryRef()

    # Transform the geometry to the target spatial reference
    geometry_28992_23032.Transform(transform_28992_23032)
    geometry_28992_4326.Transform(transform_28992_4326)

    # Get the transformed coordinates
    x = round(geometry_28992_23032.GetX(), 4)
    y = round(geometry_28992_23032.GetY(), 4)
    lat = round(geometry_28992_4326.GetX(), 5)
    lon = round(geometry_28992_4326.GetY(), 5)

    # Write the transformed feature to the output CSV file
    csv_writer.writerow(attributes + [x, y, lon, lat])

# Close the datasets
input_dataset = None
output_dataset.close()

print("Reprojection completed.")
