import math


class TileCoordinateConverter:
    """
    Based on The bounding box is defined by the top-left and bottom-right coordinates
    from openstreetmap we can calculate the tiles within the bounding box.
    """
    def __init__(self, top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon, zoom=17):
        self.zoom = zoom
        self.top_left_lat = top_left_lat
        self.top_left_lon = top_left_lon
        self.bottom_right_lat = bottom_right_lat
        self.bottom_right_lon = bottom_right_lon

    def LonLat2tile(self, lat_deg, lon_deg, zoom=None):
        """
        Convert latitude and longitude to tile coordinates
        :param lat_deg:
        :param lon_deg:
        :param zoom:
        :return:
        """
        if zoom is None:
            zoom = self.zoom

        # Convert latitude and longitude to radians
        lat_rad = math.radians(lat_deg)
        n = 2.0 ** zoom
        xtile = int((lon_deg + 180.0) / 360.0 * n)
        ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
        return (xtile, ytile)

    def get_tiles_in_bbox(self, zoom=None) ->  list[tuple[int, int]]:
        """
        Get all tiles within the bounding box
        :param top_left_lat:
        :param top_left_lon:
        :param bottom_right_lat:
        :param bottom_right_lon:
        :param zoom:
        :return:
        """
        if zoom is None:
            zoom = self.zoom

        top_left_tile = self.LonLat2tile(self.top_left_lat, self.top_left_lon, zoom)
        bottom_right_tile = self.LonLat2tile(self.bottom_right_lat, self.bottom_right_lon, zoom)
        #
        # print(f'top_left_tile: {top_left_tile}')
        # print(f'bottom_right_tile: {bottom_right_tile}')
        #
        # tiles = []
        # for x in range(top_left_tile[0], bottom_right_tile[0] + 1):
        #     for y in range(top_left_tile[1], bottom_right_tile[1] + 1):
        #         tiles.append((x, y))
        #         print(f'x: {x}, y: {y}')
        # return tiles

        #top_left_tile = self.LonLat2tile(57.0516, 9.9142, 17)
        #bottom_right_tile = self.LonLat2tile(57.0425, 9.9348, 17)

        tiles = []
        for x in range(top_left_tile[0], bottom_right_tile[0] + 1):
            #print(f'top_left_tile[0], bottom_right_tile[0] + 1: {top_left_tile[0], bottom_right_tile[0] + 1}')
            #print(f'top_left_tile[1], bottom_right_tile[1] + 1: {top_left_tile[1], bottom_right_tile[1] + 1}')
            #print(f'x: {x}')
            for y in range(top_left_tile[1], bottom_right_tile[1] + 1):
                tiles.append((x, y))
               # print(f'x: {x}, y: {y}')
        return tiles


# Define the bounding box (top left and bottom right coordinates)
#top_left_lat = 57.0516
#top_left_lon = 9.9142
#bottom_right_lat = 57.0425
#bottom_right_lon = 9.9348


top_left_lat = 57.0537
top_left_lon = 9.9104

bottom_right_lat = 57.0393
bottom_right_lon = 9.9331

if __name__ == "__main__":
    converter = TileCoordinateConverter(top_left_lat, top_left_lon, bottom_right_lat, bottom_right_lon)
    print(len(converter.get_tiles_in_bbox()))
