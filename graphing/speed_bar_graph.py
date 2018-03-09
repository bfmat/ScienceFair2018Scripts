#!/usr/bin/env python3

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from graph_configuration import *

# A tool for graphing trials at multiple speeds in a multicolored bar graph
# Created by brendon-ai, March 2018

# Colors to graph the series in
COLORS = ['red', 'yellow', 'green', 'blue']

# Speeds of the various series, in kilometers per hour
SPEEDS = [5, 8, 12, 15]

# A list of lists containing each of the data points arranged by speeds, where None is a failure
DATA_POINTS_BY_SPEED = [
    [40.4],
    [44.5, 39.2, 44.6, None, 21.7, 20.6, None, None, 33.9, 21.4, 49.2, 22.6, 19.3, 18.4, 19.9, None, 19.4, 18.9, 23.6,
     None, 34.4, 31.9, 16.9, None, 19.2, 17.4, 15.3],
    [21.1, 20.2],
    [None, 23.3, 18.2]
]

# Create a figure and set the window and graph titles
plt.figure('Speed Bar Graph')
plt.suptitle('Positional Standard Deviation by Trials and Speeds', fontsize=TITLE_SIZE)
# Set the subplot's X and Y axis labels
plt.ylabel('Standard Deviation from Center of Image (Pixels)', fontsize=AXIS_LABEL_SIZE, labelpad=AXIS_LABEL_PADDING)
plt.xlabel('Trial', fontsize=AXIS_LABEL_SIZE, labelpad=AXIS_LABEL_PADDING)
# Set the tick font size
plt.tick_params(labelsize=TICK_LABEL_SIZE, pad=TICK_LABEL_PADDING)

# Create a list of all of the data points to graph in a single list, and a list for corresponding colors
graph_points_unsorted = []
colors_for_data_points = []
# Create a list to hold the items to be added to the legend
legend_handles = []
# Iterate over the lists of data points and corresponding speeds, colors, and horizontal indices
for points, speed, color in zip(DATA_POINTS_BY_SPEED, SPEEDS, COLORS):
    # Create a legend handle containing the color and the speed
    handle = Patch(color=color, label='{} km/h'.format(speed))
    legend_handles.append(handle)
    # Iterate over the points of the current speed
    for point in points:
        # Add the value to the list of points to graph, replacing None with 0
        graph_point = 0 if point is None else point
        graph_points_unsorted.append(graph_point)
    # Add the same number of copies of the current color to the list of colors
    colors_for_data_points += [color] * len(points)
# Graph these points and colors on the plot, numbered from 0 to one less than however many there are
plt.bar(range(len(graph_points_unsorted)), graph_points_unsorted, color=colors_for_data_points)

# Iterate over the bars that were drawn, and the corresponding unsorted graph points, adding labels
for point, bar in zip(graph_points_unsorted, plt.gca().patches):
    # Get the X and Y positions of the center of the top of the bar
    x = bar.get_x() + (bar.get_width() / 2)
    y = bar.get_height()
    # Draw a label at this point, substituting 0 with Fail
    label_text = 'Fail' if point == 0 else point
    plt.text(x, y, label_text, ha='center', va='bottom')

# Set up the legend and display the completed graph
plt.legend(handles=legend_handles, fontsize=LEGEND_SIZE)
plt.show()
