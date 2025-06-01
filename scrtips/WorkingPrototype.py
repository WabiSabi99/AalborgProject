import osmnx as ox
import networkx as nx
from shapely.geometry import Point

from pyrosm_aalborg import PathPlot

# Parse the OSM XML data
graph = ox.graph_from_xml("../bounding_box_map_aalborg.osm", simplify=False)

# Filter the graph to include only drivable roads
drivable_graph = ox.project_graph(ox.utils_graph.truncate.largest_component(graph, strongly=True),
                                  to_crs="EPSG:4326")  # Project to EPSG:4326 for filtering

print(drivable_graph)


# Convert the graph to geopandas GeoDataFrames
gdf_nodes, gdf_edges = ox.graph_to_gdfs(drivable_graph, nodes=True, edges=True, node_geometry=False,
                                        fill_edge_geometry=True)

# Create a new graph from the GeoDataFrames
drivable_graph = ox.graph_from_gdfs(gdf_nodes, gdf_edges)

print(drivable_graph)

# If you want the graph to be directed
drivable_graph = drivable_graph.to_directed()


# Define the heuristic function (Euclidean distance)
def heuristic(a, b):
    (x1, y1) = drivable_graph.nodes[a]['y'], drivable_graph.nodes[a]['x']
    (x2, y2) = drivable_graph.nodes[b]['y'], drivable_graph.nodes[b]['x']
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


# Define the start and end coordinates (longitude, latitude)
start_lng, start_lat = 57.05350483704389, 9.910718278372267
end_lng, end_lat = 57.043652212110054, 9.932369902584401

# Find the nearest nodes to the start and end coordinates
start_node = ox.nearest_nodes(drivable_graph, start_lat, start_lng)
end_node = ox.nearest_nodes(drivable_graph, end_lat, end_lng)

# Find the shortest path using A*
path = nx.astar_path(drivable_graph, start_node, end_node, heuristic=heuristic)

print("Path:", path)

# Convert node IDs to coordinates
path_coords = [(drivable_graph.nodes[node]['y'], drivable_graph.nodes[node]['x']) for node in path]


# Calculate the total distance of the path
total_distance = sum(drivable_graph.get_edge_data(u, v)[0]['length'] for u, v in nx.utils.pairwise(path))

# Convert distance to kilometers
total_distance_km = total_distance / 1000

# Calculate the estimated time to walk the path (in seconds)
average_walking_speed_m_per_s = 1.4
estimated_time_s = total_distance / average_walking_speed_m_per_s

# Convert estimated time to minutes
estimated_time_min = estimated_time_s / 60

print(f"Total distance: {total_distance_km} km")
print(f"Estimated time: {estimated_time_min} minutes")

pathplot = PathPlot(path_coords, "../output.osm.pbf")
pathplot.plot()
