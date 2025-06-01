import osmnx as ox
from osm_to_graph import OSMToGraph
from NodeLocator import NodeLocator
from PathAStar import AStarSearch
from pyrosm_aalborg import PathPlot


# Define the heuristic function (custom heuristic cost)
def heuristic(graph, a, b):
    (x1, y1) = graph.nodes[a]['y'], graph.nodes[a]['x']
    (x2, y2) = graph.nodes[b]['y'], graph.nodes[b]['x']
    # Calculate the custom heuristic cost based on Euclidean distance
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def main():
    # Load the drivable graph of Aalborg
    osm_to_graph = OSMToGraph("../bounding_box_map_aalborg.osm", "ImageMetaDataSetWithNodeID2.csv")
    drivable_graph = osm_to_graph.drivable_graph

    NodeFinder = NodeLocator(drivable_graph)

    image_lat = 57.0541606239178
    image_lon = 9.91177974027744

    print(f"node x and y: {image_lat}, {image_lon}")
    print("ox implementation", ox.nearest_nodes(drivable_graph, image_lat, image_lon))
    print("custom code", NodeFinder.find_closest_node(image_lat, image_lon))

    # Define the start and end coordinates (longitude, latitude)
    start_lng, start_lat = 57.048028567059944, 9.928551711992268
    end_lng, end_lat = 57.042687231664424, 9.919960880191109

    start_node = NodeFinder.find_closest_node(start_lat, start_lng)
    end_node = NodeFinder.find_closest_node(end_lat, end_lng)

    PathStar_object = AStarSearch(drivable_graph, start_node, end_node, osm_to_graph.custom_cost)

    path = PathStar_object.a_star_search()

    print("Path:", path)

    # Convert node IDs to coordinates
    path_coords = [(drivable_graph.nodes[node]['y'], drivable_graph.nodes[node]['x']) for node in path]

    # path_coords = [[drivable_graph.nodes[node]['x'], drivable_graph.nodes[node]['y']] for node in path]

    # need to have get coords like  [[,y,x],[,y,x],[,y,x]]

    print( path_coords)



    # Calculate the total distance of the path
    total_distance = sum(drivable_graph.get_edge_data(u, v)[0]['length'] for u, v in zip(path[:-1], path[1:]))


    # Convert distance to kilometers
    total_distance_km = total_distance / 1000

    # Calculate the estimated time to walk the path (in seconds)
    average_walking_speed_m_per_s = 1.4
    estimated_time_s = total_distance / average_walking_speed_m_per_s

    # Convert estimated time to minutes
    estimated_time_min = estimated_time_s / 60

    print(f"Total distance: {total_distance_km} km")
    print(f"Estimated time: {estimated_time_min} minutes")

    pathplot = PathPlot(path_coords, "output.osm.pbf")

    pathplot.plot()


if __name__ == "__main__":
    main()
