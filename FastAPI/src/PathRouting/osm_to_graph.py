import osmnx as ox
import pandas as pd
import networkx as nx


class OSMToGraph:
    def __init__(self, file_path, node_ids_file):
        # Read the node IDs from the CSV file
        self.node_ids_df = pd.read_csv(node_ids_file)
        self.node_ids_to_keep = set(self.node_ids_df['Node ID'].values)

        # Load the OSM data
        osm_data = ox.graph_from_xml(file_path, simplify=False)

        # Filter the nodes
        nodes_to_keep = {node for node in osm_data.nodes if node in self.node_ids_to_keep}

        # Create a subgraph with the filtered nodes
        self.graph = osm_data.subgraph(nodes_to_keep).copy()

        # Project the graph to WGS84 CRS
        self.drivable_graph = ox.project_graph(self.graph, to_crs="EPSG:4326")

    def initialize_custom_cost_value(self):
        try:
            # Read custom data from CSV file and store it as node attributes
            custom_data_df = self.node_ids_df
            # Iterate over rows in the DataFrame and add custom data as attributes to nodes
            for index, row in custom_data_df.iterrows():
                node_id = row['Node ID']

                if node_id in self.drivable_graph.nodes:
                    custom_values = {
                        'city_infrastructure': row.get('City infrastructure', 0),
                        'residential_zone': row.get('Residential Zone', 0),
                        'commercial_zone': row.get('Commercial Zone', 0),
                        'entertainment_zone': row.get('Entertainment Zone', 0),
                        'nature': row.get('Nature', 0),
                        'harbour': row.get('Harbour', 0),
                        'culture': row.get('Culture', 0)
                    }
                    self.drivable_graph.nodes[node_id].update(custom_values)
        except FileNotFoundError:
            print("Error: Could not read the custom data CSV file.")
            return

    def custom_cost(self, node1, node2):
        u = self.drivable_graph.nodes[node1]
        v = self.drivable_graph.nodes[node2]

        # Calculate the distance between the nodes
        distance = ((u['y'] - v['y']) ** 2 + (u['x'] - v['x']) ** 2) ** 0.5

        # Check if the 'highway' key exists in the edge data
        edge_data = self.drivable_graph.edges[node1, node2, 0]
        road_type_factor = 2  # Default factor

        if 'highway' in edge_data:
            road_type = edge_data['highway']
            if road_type in ['motorway', 'trunk']:
                road_type_factor = 10
            elif road_type == 'primary':
                road_type_factor = 3
            elif road_type == 'secondary':
                road_type_factor = 2

        if 'footway' in edge_data or 'pedestrian' in edge_data or 'path' in edge_data:
            road_type_factor = 1  # Lowest cost factor for walkable paths

        return distance * road_type_factor

    def modify_graph(self):
        # Modify the graph by assigning custom weights to the edges
        for u, v, k, data in self.drivable_graph.edges(keys=True, data=True):
            data['weight'] = self.custom_cost(u, v)

    def get_graph(self):
        return self.drivable_graph


if __name__ == "__main__":
    # Assuming the paths to the files are correctly provided
    osm_to_graph = OSMToGraph("../bounding_box_map_aalborg.osm", "ImageMetaDataSetWithNodeID2.csv")
    osm_to_graph.modify_graph()
    drivable_graph = osm_to_graph.get_graph()
    # Initialize custom cost values if needed
    osm_to_graph.initialize_custom_cost_value("ImageMetaDataSetWithNodeID.csv")
    print(drivable_graph.nodes(data=True))
    # print(drivable_graph.edges(data=True))
