from starlette.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import signal
import fastapi
from fastapi.responses import JSONResponse
import uvicorn
import geojson
from typing import Tuple

from PathRouting.osm_to_graph import OSMToGraph
from PathRouting.NodeLocator import NodeLocator
from PathRouting.PathAStar import AStarSearch
from PathRouting.FastapiBaseModels import *

app = fastapi.FastAPI()

debug = True

origins = [
    "http://localhost",
    "http://localhost:8000",
]

# Declare the variables at the global level
osm_to_graph = None
drivable_graph = None


@app.on_event("startup")
async def startup_event():
    global osm_to_graph, drivable_graph
    # Define drivable_graph at the global level
    osm_to_graph = OSMToGraph("bounding_box_map_aalborg.osm")
    drivable_graph = osm_to_graph.drivable_graph


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/html", StaticFiles(directory="static/html"), name="html")
app.mount("/images", StaticFiles(directory="static/images"), name="images")
app.mount("/javascript", StaticFiles(directory="static/javascript"), name="javascript")
app.mount("/javascript/geodata", StaticFiles(directory="static/javascript/geodata"), name="geodata")


async def hello():
    return fastapi.Response(status_code=200, content='Hello, world!')


@app.get("/")
async def redirect_to_html():
    return RedirectResponse(url="/html/index.html")


@app.post("/api/get_path")
async def get_path(pathCoords: PathCoords):
    global osm_to_graph, drivable_graph

    # Extract start and end positions from the PathCoords instance
    startPos = pathCoords.startPos
    endPos = pathCoords.endPos

    NodeFinder = NodeLocator(drivable_graph)

    # Find the closest nodes to the start and end positions
    start_node = NodeFinder.find_closest_node(startPos['y'], startPos['x'])
    end_node = NodeFinder.find_closest_node(endPos['y'], endPos['x'])

    if debug:
        print(f"Received request for path from {startPos} to {endPos}")
        print(f"Start node: {start_node}, End node: {end_node}")

    import time

    start = time.time()

    # Perform A* search to find the path
    PathStar_object = AStarSearch(drivable_graph, start_node, end_node, osm_to_graph.custom_cost)

    path = PathStar_object.a_star_search()

    print(f'time taken to run path a star: {time.time() - start} seconds')

    # Convert node IDs to coordinates
    path_coords = [(drivable_graph.nodes[node]['x'], drivable_graph.nodes[node]['y']) for node in path]

    # Return the path as the response
    return path_coords


async def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return fastapi.Response(status_code=200, content='Server shutting down...')


@app.on_event("shutdown")
def on_shutdown():
    print('Server shutting down...')


app.add_api_route('/hello', hello, methods=['GET'])
app.add_api_route('/shutdown', shutdown, methods=['GET'])

if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8000, reload=True, reload_dirs=["src"], log_level="info")
