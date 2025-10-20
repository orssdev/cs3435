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
    return image