import pandas as pd
import json

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('../deduplicated_data.csv', names=['Image Name', 'ID', 'Face', 'Build ID', 'Latitude', 'Longitude', 'Capture date', 'image_url', 'Has Blurs', 'tile_URL', 'Coverage Type', 'Image tile', 'Street Address'])

def convert_to_geojson(df):
    features = []
    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "properties": {
                "id": row['ID'].split('_')[0],
                "image_name": row['Image Name'],
                "face": row['Face'],
                "build_id": row['Build ID'],
                "capture_date": row['Capture date'],
                "image_url": row['image_url'],
                "has_blurs": row['Has Blurs'],
                "tile_url": row['tile_URL'],
                "coverage_type": row['Coverage Type'],
                "image_tile": row['Image tile'],
                "address": row['Street Address']
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row['Longitude'], row['Latitude']]
            }
        }
        features.append(feature)
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson

# Convert the DataFrame to GeoJSON
geojson_data = convert_to_geojson(df)

# Save the GeoJSON data to a file
with open('output_smaller.geojson', 'w') as file:
    json.dump(geojson_data, file, indent=2)