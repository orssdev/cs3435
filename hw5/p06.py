import matplotlib.pyplot as plt
import numpy as np


def construct_file_name(lat, lon):
    """ Takes the latitude and longitude as signed integers and
    constructs the appropriate file name for the TIF file. """
    file_name = f'USGS_NED_1_{'n' if lat > 0 else 's'}{f'{abs(lat):02}'}{'e' if lon > 0 else 'w'}{f'{abs(lon):03}'}_IMG.tif'
    return file_name

print(construct_file_name(lat=36, lon=-82))
print(construct_file_name(lat=-36, lon=82))
print(construct_file_name(lat=-0, lon=0))

# im = plt.imread('USGS_NED_1_n36w082_IMG.tif')
# print(type(im))
# print(im.shape)

# plt.imshow(im)
# plt.show()