#!/usr/bin/env python3

import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# Load a heat map image for each road line, combine them, and render a 3D graph of the road that looks like a half pipe,
# where the middle is low because the network's responses are low, and the edges of the road are peaks
# Created by brendon-ai, February 2018

# Check that the number of command line arguments is correct
if len(sys.argv) != 3:
    print('Usage:', sys.argv[0], '<left line heat map> <right line heat map>')
    sys.exit()

# Load the left and right heat maps and add them together to create an overall heat map
heat_map = sum(plt.imread(os.path.expanduser(path)) for path in sys.argv[1:])
# Create matrices of X and Y values which contain all coordinates in the heat map
x_values, y_values = np.meshgrid(range(heat_map.shape[1]), range(heat_map.shape[0]))
# Get the Z values, which are the heat values at the X and Y positions
z_values = heat_map[y_values, x_values]

# Create a 3D figure with a specified title and plot the points
fig = plt.figure('Heat Map Render')
ax = Axes3D(fig)
surface = ax.plot_surface(
    # Use the computed X, Y, and Z values
    X=x_values,
    Y=y_values,
    Z=z_values,
    # Use strides of 1 so no points are skipped
    rstride=1,
    cstride=1,
    # Use heat map colors where red is at the top of the graph and blue is at the bottom
    cmap=cm.coolwarm
)
# Set the axis titles to describe their meaning
ax.set_xlabel('X Position in Heat Map')
ax.set_ylabel('Y Position in Heat Map')
ax.set_zlabel('Total Output Activation')
# Add a color bar to the figure that acts as a legend for the heat values, using a shrink of 0.5 so it doesn't take up
# the entire window vertically, and a height to width ratio of 8 so it isn't too narrow
fig.colorbar(surface, shrink=0.5, aspect=8)
# Display the graph on screen
plt.show()
