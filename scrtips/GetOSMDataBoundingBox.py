import requests

# Define the bounding box coordinates
top_left_lat = 57.0537
top_left_lon = 9.9104
bottom_right_lat = 57.0393
bottom_right_lon = 9.9331

# Construct the Overpass query
query = f"""
[bbox:{bottom_right_lat},{top_left_lon},{top_left_lat},{bottom_right_lon}]
[out:json]
[timeout:90];
(
    node;
    way;
    relation;
);
out geom;
"""

# Send the query to the Overpass API
url = "https://overpass-api.de/api/interpreter"
response = requests.post(url, data={"data": query})

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # print(data)

    # save the data to a file
    with open("osm_data_aalborg.osm", "w", encoding='utf-8') as f:
        f.write(response.text)

else:
    print(f"Error: {response.status_code} - {response.text}")