#!/usr/bin/env python3

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate

# Load a heat map image for each road line, combine them, and render a 3D graph of the road that looks like a half pipe,
# where the middle is low because the network's responses are low, and the edges of the road are peaks
# Created by brendon-ai, February 2018

# Font sizes for the various parts of the UI
TITLE_SIZE = 24
AXIS_LABEL_SIZE = 16
TICK_LABEL_SIZE = 12

# The stride with which the interpolation of the X and Y values is done
INTERPOLATION_STRIDE = 0.1

# Check that the number of command line arguments is correct
if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<left line heat map> <right line heat map>')
    sys.exit()

# Load the left and right heat maps and add them together to create an overall heat map
heat_map = sum(plt.imread(os.path.expanduser(path)) for path in sys.argv[1:])
# Create matrices of X and Y values which contain all coordinates in the heat map
x_values, y_values = np.mgrid[0:heat_map.shape[1], 0:heat_map.shape[0]]
# Get the Z values, which are the heat values at the X and Y positions
z_values = heat_map[y_values, x_values]

# Create matrices of X and Y values which contain all coordinates in the heat map as well as points interpolated between
# with a predefined stride of 0.5; these are used to interpolate Z values and synthesize a higher-resolution surface
x_values_interpolated, y_values_interpolated = \
    np.mgrid[0:heat_map.shape[1]:INTERPOLATION_STRIDE, 0:heat_map.shape[0]:INTERPOLATION_STRIDE]
# Fit a spline surface to the original points, and interpolate the Z values accordingly
tck = interpolate.bisplrep(x_values, y_values, z_values, kx=4, ky=4, s=70)
z_values_interpolated = interpolate.bisplev(x_values_interpolated[:, 0], y_values_interpolated[0, :], tck)

# Create a 3D figure with a specified title and size
fig = plt.figure('Heat Map Render', figsize=(16, 12))
ax = Axes3D(fig)
# Set the tick font size
plt.tick_params(labelsize=TICK_LABEL_SIZE)
# Set the axis titles to describe their meaning
ax.set_xlabel('X Position in Heat Map', fontsize=AXIS_LABEL_SIZE)
ax.set_ylabel('Y Position in Heat Map', fontsize=AXIS_LABEL_SIZE)
ax.set_zlabel('Total Output Activation', fontsize=AXIS_LABEL_SIZE)

# Plot the points in 3D
surface = ax.plot_surface(
    # Use the interpolated X, Y, and Z values
    X=x_values_interpolated,
    Y=y_values_interpolated,
    Z=z_values_interpolated,
    # Use strides of 1 so no points are skipped
    rstride=1,
    cstride=1,
    # Use heat map colors where red is at the top of the graph and blue is at the bottom
    cmap=cm.coolwarm
)

# Add a color bar to the figure that acts as a legend for the heat values, using a shrink of 0.75 so it doesn't take up
# the entire window vertically, and a height to width ratio of 12 so it isn't too narrow
cbar = fig.colorbar(surface, shrink=0.75, aspect=12)
# Set the font size of the ticks on the color bar
cbar.ax.tick_params(labelsize=TICK_LABEL_SIZE)
# Display the graph on screen
plt.show()
