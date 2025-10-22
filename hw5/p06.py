import matplotlib.pyplot as plt
import numpy as np


def construct_file_name(lat, lon):
    """ Takes the latitude and longitude as signed integers and
    constructs the appropriate file name for the TIF file. """
    file_name = f'USGS_NED_1_{'n' if lat > 0 else 's'}{f'{abs(lat):02}'}{'e' if lon > 0 else 'w'}{f'{abs(lon):03}'}_IMG.tif'
    return file_name


def load_trim_image(lat, lon):
    """ Takes the latitude and longitude as signed integers and
    loads the appropriate file. It then trims off the boundary
    of six pixels on all four sides. """
    image = plt.imread(construct_file_name(lat, lon))
    return image[6:-6, 6:-6]


def stitch_four(lat, lon):
    # load the four images and construct the resulting image:
    # (nw_lat, nw_lon), (nw_lat, nw_lon+1)
    # (nw_lat-1, nw_lon), (nw_lat-1, nw_lon+1)
    image1 = load_trim_image(lat, lon)
    image2 = load_trim_image(lat, lon + 1)
    image3 = load_trim_image(lat - 1, lon)
    image4 = load_trim_image(lat - 1, lon + 1)
    top = np.concatenate([image1, image2], axis=1)
    bottom = np.concatenate([image3, image4], axis=1)
    image = np.concatenate([top, bottom])
    return image


def get_row(lat, lon_min, num_tiles):
    """ Takes the latitude, minimum longitude, and number of tiles and
    returns an image that combines tiles along a row of different
    longitudes. """
    images = []
    for i in range(num_tiles):
        images.append(load_trim_image(lat, lon_min + i))
    image = images[0]
    for img in images[1:]:
        image = np.concatenate([image, img], axis=1)
    return image


def get_tile_grid(lat_max, lon_min, num_lat, num_lon):
    """ Takes the northwest coordinate (maximum latitude, minimum longitude)
    and the number of tiles in each dimension (num_lat, num_lon) and
    constructs the image containing the entire range. """
    rows = []
    for i in range(num_lat):
        rows.append(get_row(lat_max - i, lon_min, num_lon))
    image = rows[0]
    for row in rows[1:]:
        image = np.concatenate([image, row])
    return image


def floor(x):
    if x >= 0:
        return int(x)
    else:
        return int(x) - (x != int(x))


def ceil(x):
    if x >= 0:
        return int(x) + (x != int(x))
    else:
        return int(x)


def get_northwest(lat, lon):
    """ Get the integer coordinates of the northwest corner of the tile
    that contains this decimal (lat, lon) coordinate. """
    nw_lat = ceil(lat) if lat > 0 else floor(lat)
    nw_lon = ceil(lon) if lon > 0 else floor(lon)
    return nw_lat, nw_lon


# def get_tile_grid_decimal(northwest, southeast):
#     """ Construct the tiled grid of TIF images that contains these
#     northwest and southeast decimal coordinates. Each corner
#     is a tuple, (lat, lon). """
#     nw_lat, nw_log = get_northwest(northwest[0], northwest[1])
#     nw_lat, nw_log = get_northwest(southeast[0], southeast[1])
#     return image