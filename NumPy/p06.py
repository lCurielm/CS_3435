import matplotlib.pyplot as plt
import numpy as np

im = plt.imread('USGS_NED_1_n36w082_IMG.tif')
print(type(im))
print(im.shape)
plt.imshow(im)
plt.show()
