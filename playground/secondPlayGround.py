import io
import sys

from streetlevel import lookaround
from pillow_heif import register_heif_opener
from PIL import Image
import time

# Register the HEIF opener
register_heif_opener()

# 57.048028567059944, 9.928551711992268

panos = lookaround.get_coverage_tile_by_latlon(57.048028567059944, 9.928551711992268)
print(f"""
Got {len(panos)} panoramas. Here's one of them:
ID: {panos[0].id}\t\tBuild ID: {panos[0].build_id}
Latitude: {panos[0].lat}\tLongitude: {panos[0].lon}
Capture date: {panos[0].date}
""")

pano = panos[0]

print(pano)

# start timer
print("Starting the script for zoom level: ", i)

seconds = time.time()

auth = lookaround.Authenticator()
faces = []
zoom = 1
for face_idx in range(0, 6):
    face_heic = lookaround.get_panorama_face(pano, face_idx, zoom, auth)

    # Convert the HEIC file to a PIL image
    # face = Image.open(face_heic)

    face = Image.open(io.BytesIO(face_heic))

    faces.append(face)

result = lookaround.to_equirectangular(faces, pano.camera_metadata)
result.save(f"{pano.id}_{zoom}.jpg", options={"quality": 100})

# end timer
print("Time taken to run the script: ", time.time() - seconds, " seconds, for zoom level: ", i)
