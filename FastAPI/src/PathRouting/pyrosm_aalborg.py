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

    def OSM_PARSER(self, ):
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
        self.drive_net.plot(ax=ax, color='#41514a', linewidth=0.5)

        # we need to move around so its (9.9175356, 57.0525453) instead of (57.0525453, 9.9175356)
        path_coords = [(coord[1], coord[0]) for coord in self.path_coords]

        # Extract x and y coordinates from path_coords
        path_x, path_y = zip(*path_coords)

        ax.set_facecolor('#f0f0f0')  # Light gray background

        # Plot the path of the star
        ax.plot(path_x, path_y, color='blue', linestyle='--', linewidth=2.5, label='Star Path')

        # Set plot title
        ax.set_title('Path A Star  in Aalborg', fontsize=14, fontweight='bold')


        # start will be green and end will be red
        ax.plot(path_x[0], path_y[0], marker='o', markersize=10, color='green', label='Start')
        ax.plot(path_x[-1], path_y[-1], marker='o', markersize=10, color='red', label='Goal')

        ax.text(path_x[0], path_y[0], 'Start', fontsize=12, fontweight='bold')
        ax.text(path_x[-1], path_y[-1], 'Goal', fontsize=12, fontweight='bold')



        # Add a legend
        ax.legend(loc='upper right')

        # ax.set_aspect('equal', adjustable='datalim')
        ax.autoscale(enable=True, axis='both', tight=True)


        # Show the plot
        plt.show()


if __name__ == "__main__":
    # test example of creating a node
    path_coordinates = [(57.0481397, 9.9286385), (57.0482463, 9.9283466), (57.048081, 9.9281912), (57.0480266, 9.92814),
                   (57.0479711, 9.9280897), (57.0479134, 9.9280367), (57.0478496, 9.9278702), (57.0476821, 9.9276838),
                   (57.0476388, 9.9275231), (57.0474728, 9.9273366), (57.0474317, 9.9272885), (57.0474055, 9.9272609),
                   (57.0473884, 9.9272214), (57.0473737, 9.927172), (57.0473663, 9.9270418), (57.0473839, 9.9269409),
                   (57.0473864, 9.926924), (57.0473889, 9.9269097), (57.0474041, 9.926821), (57.0474821, 9.9263648),
                   (57.0475511, 9.9259619), (57.0475907, 9.9257303), (57.0475573, 9.9257015), (57.0474799, 9.9256556),
                   (57.0469892, 9.9253608), (57.0466776, 9.9251816), (57.0466745, 9.9251217), (57.0467404, 9.9245026),
                   (57.0467635, 9.9242175), (57.0467701, 9.92414), (57.0467715, 9.9240945), (57.0468172, 9.923793),
                   (57.046863, 9.9235111), (57.0468901, 9.9233507), (57.0469065, 9.9232997), (57.0468744, 9.9232898),
                   (57.0469146, 9.9230896), (57.047032, 9.9225043), (57.0471517, 9.9219576), (57.047296, 9.921354),
                   (57.0473239, 9.9212359), (57.0474551, 9.920698), (57.0474964, 9.920597), (57.0475571, 9.9201987),
                   (57.0475811, 9.9200468), (57.0476122, 9.9198435), (57.047657, 9.9195816), (57.0477067, 9.9193422),
                   (57.0477199, 9.9192703), (57.0477474, 9.9191372), (57.0477821, 9.9189653), (57.0478086, 9.918814),
                   (57.0478246, 9.9186962), (57.0478315, 9.9186361), (57.0479244, 9.9182692), (57.0479794, 9.9182406),
                   (57.0480123, 9.9179717), (57.0480838, 9.9175734), (57.0481754, 9.9172927), (57.0482042, 9.9171756),
                   (57.0482884, 9.9166401), (57.0483411, 9.9160734), (57.0483553, 9.9159178), (57.04836, 9.9158662),
                   (57.0482989, 9.9158324), (57.0482225, 9.9157744), (57.0480122, 9.9155461), (57.0479099, 9.9154605),
                   (57.0478062, 9.915372), (57.0475847, 9.9151449), (57.0475129, 9.915109), (57.0474527, 9.9150464),
                   (57.0472228, 9.9147756), (57.0471777, 9.9147208), (57.0471249, 9.9146565), (57.0470625, 9.9145806),
                   (57.0469012, 9.9142677), (57.0468726, 9.9142274), (57.0467648, 9.9140704), (57.0466847, 9.9139401),
                   (57.0466198, 9.9138277), (57.0465581, 9.9137058), (57.0465164, 9.9136356), (57.0464735, 9.9135685),
                   (57.0464136, 9.9135342), (57.0463751, 9.9135095), (57.0462653, 9.9134038), (57.0462305, 9.9133719),
                   (57.0459997, 9.9131649), (57.0457142, 9.9129106), (57.0454891, 9.9127259), (57.0453631, 9.9126314),
                   (57.0448111, 9.9122679), (57.0447549, 9.9122305), (57.0446665, 9.9121717), (57.0446491, 9.9122603),
                   (57.0441735, 9.9119036), (57.0437686, 9.9117601), (57.0435231, 9.9116347), (57.0434031, 9.9115583),
                   (57.0433126, 9.9115428), (57.0431784, 9.911457), (57.0430784, 9.9113671), (57.0429945, 9.9112746),
                   (57.0425538, 9.9111325)]
    data = "../bounding_box_map_aalborg.osm.pbf"
    path_plot = PathPlot(path_coordinates, data)
    path_plot.plot()
