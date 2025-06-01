import numpy as np


class NodeLocator:
    def __init__(self, graph):
        self.graph = graph



    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points
        on the Earth's surface using the Haversine formula.
        :param lat1: Latitude of the first point
        :param lon1: Longitude of the first point
        :param lat2: Latitude of the second point
        :param lon2: Longitude of the second point
        :return: Distance between the two points in meters
        """
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = np.radians([lat1, lon1, lat2, lon2])

        # Haversine formula
        difference_lon = lon2 - lon1  # Difference in longitude
        difference_lat = lat2 - lat1  # Difference in latitude
        a = np.sin(difference_lat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(difference_lon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        radius = 6371000  # Radius of the Earth in meters
        distance = radius * c

        return distance

    def find_closest_node(self, latitude, longitude):
        """
        Find the closest node in the graph to the given latitude and longitude.
        :param latitude: Latitude of the target location
        :param longitude: Longitude of the target location
        :return: Node ID of the closest node
        """
        closest_node = None
        min_distance = float('inf')

        for node in self.graph.nodes(data=True):
            # print(node.__class__)
            node_id, data = node
            # print(node)
            node_lat = data['x']
            node_lon = data['y']
            distance = self.haversine(latitude, longitude, node_lat, node_lon)
            if distance < min_distance:
                min_distance = distance
                closest_node = node_id

        return closest_node
