#!/usr/bin/env python3

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from graph_configuration import *

# A tool for graphing changing characteristics over a series of trials
# Created by brendon-ai, February 2018

# Colors to graph the two series in; if there is only one, the first color is used
COLORS = ['red', 'blue']

# Ask the user for the X axis label
x_label = input('Enter the X axis label: ')
# Get the number of trials, and the number of data series per trial, from the user
num_trials = int(input('Enter the number of trials: '))
num_series = 2 if input('Enter "y" if two data series are being used: ') == 'y' else 1
# Get the numbers of the trials
print('Enter the numbers of the {} trials, each on a separate line:'.format(num_trials))
trial_numbers = [int(input().strip()) for _ in range(num_trials)]

# Create a dictionary of the value lists for each series
values_by_trial = {}
# Iterate over the subplots and corresponding trial names
for series_index in range(num_series):
    # Ask the user for the name of this data series
    series_name = input('Enter the name of data series {}: '.format(series_index))
    # Collect every data point in this series, each on a separate line
    print('Enter the {} data points, each on a separate line:'.format(num_trials))
    series_values = [float(input().strip()) for _ in range(num_trials)]
    # Add it to the dictionary under the corresponding trial name
    values_by_trial[series_name] = series_values

# Create a figure and add a subplot, duplicating its X axis into a different plot if there are two series
fig = plt.figure('Trials Graph')
subplots = [fig.add_subplot(111)]
if num_series == 2:
    subplots.append(subplots[0].twinx())
# Get a title for the figure and set it
fig.suptitle(input('Enter the graph title: '), fontsize=TITLE_SIZE)
# Iterate over the subplots, series keys, and corresponding colors, creating a list of color handles
color_handles = []
for subplot, series_name, color in zip(subplots, values_by_trial.keys(), COLORS):
    # Graph the series as a line with the provided trial numbers
    subplot.plot(
        trial_numbers,
        values_by_trial[series_name],
        color=color,
        label=series_name
    )
    # Set the Y axis label with the series name
    subplot.set_ylabel(series_name, fontsize=AXIS_LABEL_SIZE, labelpad=AXIS_LABEL_PADDING)
    # Set the X axis label with the specified X axis label
    subplot.set_xlabel(x_label, fontsize=AXIS_LABEL_SIZE, labelpad=AXIS_LABEL_PADDING)
    # Set the tick font size
    subplot.tick_params(labelsize=TICK_LABEL_SIZE, pad=TICK_LABEL_PADDING)
    # Create a color handle for the legend
    color_handles.append(mpatches.Patch(color=color, label=series_name))
# Automatically generate a legend for the graph if there is more than one data series
if num_series > 1:
    plt.legend(handles=color_handles, fontsize=LEGEND_SIZE)
# Display the completed graph
plt.show()
