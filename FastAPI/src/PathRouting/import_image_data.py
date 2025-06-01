import osmnx as ox
import pandas as pd


class NodeMatcher:
    def __init__(self, graph):
        self.graph = graph

    def match_nodes(self, lon_lat_list):
        matched_nodes = []
        for lon, lat in lon_lat_list:

            try:
                # Find the nearest node in the graph to the given lat-lon coordinates
                node = ox.distance.nearest_nodes(self.graph, float(lon), float(lat))
                matched_nodes.append(node)
            except:
                print(f"Error: Could not find a node for coordinates {lon}, {lat}")

        return matched_nodes


def get_image_data_from_graph(csv_file_path, graph):
    data_frame = pd.read_csv(csv_file_path)

    # remove columns
    data_frame.drop(columns=['Build ID'], inplace=True)
    data_frame.drop(columns=['Capture date'], inplace=True)
    # Has Blurs
    data_frame.drop(columns=['Has Blurs'], inplace=True)
    # Coverage Type
    data_frame.drop(columns=['Coverage Type'], inplace=True)
    # Extract latitude and longitude coordinates from the CSV file
    lon_lat_list = data_frame[['Longitude', 'Latitude']].values.tolist()

    # Initialize the node matcher with the graph
    node_matcher = NodeMatcher(graph)

    # Match nodes from the graph to the coordinates from the CSV file
    matched_nodes = node_matcher.match_nodes(lon_lat_list)

    # Add the matched node IDs to the DataFrame
    data_frame['Node ID'] = matched_nodes

    # add new column to the dataframe

    data_frame['City infrastructure'] = 0
    data_frame['Residential Zone'] = 0
    data_frame['Commercial Zone'] = 0
    data_frame['Entertainment Zone'] = 0
    data_frame['Nature'] = 0
    data_frame['Harbour'] = 0
    data_frame['Culture'] = 0

    # # remove duplicates
    # data_frame.drop_duplicates(subset=['ImageID'], inplace=True)

    # Save the DataFrame to a new CSV file
    data_frame.to_csv("ImageMetaDataSetWithNodeID2.csv", index=False)


if __name__ == "__main__":
    # Load your graph from the OSM file
    osm_file_path = "../bounding_box_map_aalborg.osm"
    graph = ox.graph_from_xml(osm_file_path, simplify=False)

    print(graph.nodes[10916413362])

    print(f"Length of nodes: {len(graph.nodes)}")

    pd = pd.read_csv("ImageMetaDataSetWithNodeID2.csv")

    # we want to check if the number of nodes is equal to the number of rows in the csv file

    node_counter = 0
    for i in range(0, len(pd['Node ID'])):
        if pd['Node ID'][i] not in graph.nodes:
            print(f"Node ID {pd['Node ID'][i]} not found in the graph")
        else:
            node_counter += 1
    print(f"Number of nodes found in the graph: {node_counter}")


    # # Provide the path to your CSV file containing image metadata
    # csv_file_path = "../csv files/ImageMetaDataSet.csv"
    # get_image_data_from_graph(csv_file_path, graph)
    #
    # # load csv file
    # # data_frame = pd.read_csv("ImageMetaDataSetWithNodeID.csv")
    # # remove duplicates
    # # data_frame.drop_duplicates(subset=['ID'], inplace=True)
    # # # save the dataframe to a new csv file
    # # data_frame.to_csv("ImageDataSetWithNodeIDAndClassification.csv", index=False)
