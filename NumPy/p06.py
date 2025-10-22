import matplotlib.pyplot as plt
import numpy as np


def construct_file_name(lat, lon):
    if lat >= 0:
        lat_var = 'n'
    else:
        lat_var = 's'
    
    lat_abs = abs(lat)
    lat_part = f"{lat_var}{lat_abs}"
    
    if lon >= 0:
        lon_var = 'e'
    else:
        lon_var = 'w'
    
    lon_abs = abs(lon)
    lon_part = f"{lon_var}{lon_abs:03d}"
    file_name = f"USGS_NED_1_{lat_part}{lon_part}_IMG.tif"
    return file_name


# print(construct_file_name(lat=36, lon=-82))
# print(construct_file_name(lat=-36, lon=82))


def load_trim_image(lat, lon):
    file_name = construct_file_name(lat,lon)
    try:
        raw_image = plt.imread(file_name)
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return np.full((3600, 3600), -1, dtype=np.int16)
    image = raw_image[6:-6, 6:-6]
    return image

def stitch_four(lat, lon):
    im_nw = load_trim_image(lat, lon)
    im_ne = load_trim_image(lat, lon + 1)
    im_sw = load_trim_image(lat - 1, lon)
    im_se = load_trim_image(lat - 1, lon + 1)
    
    top_row = np.hstack((im_nw, im_ne))
    bot_row = np.hstack((im_sw, im_se))
    image = np.hstack((top_row, bot_row))
    return image



def get_row(lat, lon_min, num_tiles):
    tile_list = []
    for i in range(num_tiles):
        cur_lon = lon_min + i
        tile = load_trim_image(lat, cur_lon)
        tile_list.append(tile)
        image = np.hstack(tile_list)
    return image


def get_tile_grid(lat_max, lon_min, num_lat, num_lon):
    grid_rows = []
    for i in range(num_lat):
        cur_lat = lat_max - i
        stitched_row = get_row(cur_lat, lon_min, num_lon)
        grid_rows.append(stitched_row)
    image = np.vstack(grid_rows)
    return image

def get_northwest(lat, lon):
    eps = 1e-12
    def close_int(x):
        return abs(x - round(x)) < eps
    def floor_no_math(x):
        i = int(x)
        if x < 0 and x != i:
            return i - 1
        return i
    def ceil_no_math(x):
        return -floor_no_math(-x)
    if close_int(lat):
        nw_lat = int(round(lat))
    else:
        nw_lat = ceil_no_math(lat)
    if close_int(lon):
        nw_lon = int(round(lon))
    else:
        nw_lon = floor_no_math(lon)
    return nw_lat, nw_lon

def get_tile_grid_decimal(northwest, southeast):
    nw_lat_dec, nw_lon_dec = northwest
    se_lat_dec, se_lon_dec = southeast
    
    nw_tile_lat, nw_tile_lon = get_northwest(nw_lat_dec, nw_lon_dec)
    se_tile_lat, se_tile_lon = get_northwest(se_lat_dec, se_lon_dec)
    num_lat = (nw_tile_lat - se_tile_lat) + 1
    lon_min = nw_tile_lon
    lon_max = se_tile_lon 
    num_lon = (lon_max - lon_min) + 1
    image = get_tile_grid(lat_max=nw_tile_lat, lon_min=lon_min, num_lat=num_lat, num_lon=num_lon)
    return image

nw = (37.2, -82.7)
se = (36.6, -82.5)
im = get_tile_grid_decimal(nw, se)
im.shape

nw = (37.2, -83.7)
se = (36.6, -81.5)
im = get_tile_grid_decimal(nw, se)
im.shape

nw = (37.5, -82.5)
se = (36.5, -81.5)
im = get_tile_grid_decimal(nw, se)
im.shape

h, w = im.shape
im[h//2-5:h//2+5, w//2-5:w//2+5]
plt.imshow(im)
plt.colorbar()
plt.show()
