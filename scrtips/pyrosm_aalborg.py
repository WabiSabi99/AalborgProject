import matplotlib.pyplot as plt
from pyrosm import OSM

class PathPlot:
    def __init__(self, path_coords, data, network_type='all'):
        self.path_coords = path_coords
        self.data = data
        self.network_type = network_type
        self.osm = None
        self.drive_net = None


        # we need the data to be osm.pbf
        if self.data.endswith(".osm.pbf"):
            self.OSM_PARSER()
        else:
            raise ValueError("Data must be in osm.pbf format")


    def OSM_PARSER(self,):
        # Initialize the OSM parser object
        self.osm = OSM(self.data)

        # Read all drivable roads

        # - `'walking'` - `'cycling'` - `'driving'` - `'driving+service'` - `'all'`.

        self.drive_net = self.osm.get_network(network_type=self.network_type)

    def plot(self):
        # Create a figure and a set of subplots
        fig, ax = plt.subplots()

        # set size of the figure

        fig.set_size_inches(10, 10)

        # Plot the drivable roads
        self.drive_net.plot(ax=ax, color='blue', linewidth=0.5)

        # we need to move around so its (9.9175356, 57.0525453) instead of (57.0525453, 9.9175356)
        path_coords = [(coord[1], coord[0]) for coord in self.path_coords]

        # Extract x and y coordinates from path_coords
        path_x, path_y = zip(*path_coords)

        # Plot the path of the star
        ax.plot(path_x, path_y, color='red', linestyle='--', linewidth=2.5, label='Star Path')

        # Set plot title
        ax.set_title('Drivable Roads and Star Path in Aalborg', fontsize=14, fontweight='bold')

        # Set x and y labels
        ax.set_xlabel('Longitude', fontsize=12)
        ax.set_ylabel('Latitude', fontsize=12)

        # Remove the top and right spines from plot
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Add a legend
        ax.legend()

        # Show the plot
        plt.show()


if __name__ == "__main__":
    # test example of creating a node
    path_coords = [(57.048028567059944, 9.928551711992268), (57.04256558551458, 9.910990256435174)]
    data = "bounding_box_map_aalborg.osm.pbf"
    path_plot = PathPlot(path_coords, data)
    path_plot.plot()
