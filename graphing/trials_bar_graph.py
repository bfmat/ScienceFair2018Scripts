#!/usr/bin/env python3

import itertools

import matplotlib.pyplot as plt
import pandas as pd

from graph_configuration import *

# A tool for graphing changing characteristics over a series of trials
# Created by brendon-ai, February 2018

# Colors to graph the two series in; if there is only one, the first color is used
COLORS = ['red', 'blue']

# Get the number of trials, and the number of data series per trial, from the user
num_trials = int(input('Enter the number of trials: '))
num_series = 2 if input('Enter "y" if two data series are being used: ') == 'y' else 1
# Get the names of the trials
print('Enter the names of the {} trials, each on a separate line:'.format(num_trials))
trial_names = [input().strip() for _ in range(num_trials)]

# Create a dictionary of the value lists for each series and an associated list for names of the series
values_by_trial = {}
# Iterate over the subplots and corresponding trial names
for series_index in range(num_series):
    # Ask the user for the name of this data series
    series_name = input('Enter the name of data series {}: '.format(series_index))
    # Collect every data point in this series, each on a separate line
    print('Enter the names of the {} data points, each on a separate line:'.format(num_trials))
    series_values = [float(input().strip()) for _ in range(num_trials)]
    # Add it to the dictionary under the corresponding trial name
    values_by_trial[series_name] = series_values
# Create a data frame from the dictionary and set the row names to the trial names
data_frame = pd.DataFrame.from_dict(values_by_trial)
data_frame.index = trial_names

# The width to make the bars for a single trial
bar_width = 0.4
# Make the bars half as wide if there is only one series
if num_series == 1:
    bar_width /= 2
# Create a figure and add a subplot, duplicating its X axis into a different plot if there are two series
fig = plt.figure('Trials Bar Graph')
subplots = [fig.add_subplot(111)]
if num_series == 2:
    subplots.append(subplots[0].twinx())
# Get a title for the figure and set it
fig.suptitle(input('Enter the graph title: '), fontsize=TITLE_SIZE)
# Iterate over the subplots and corresponding series names, along with colors and positions for the graph
for subplot, series_name, color, position in zip(subplots, data_frame.columns.values, COLORS, itertools.count()):
    # Graph the series on the subplot
    data_frame[series_name].plot(kind='bar', color=color, ax=subplot, width=bar_width, position=position)
    # Set the subplot's Y axis label with the series name
    subplot.set_ylabel(series_name, fontsize=AXIS_LABEL_SIZE, labelpad=AXIS_LABEL_PADDING)
    # Set the X axis label with a hardcoded value
    subplot.set_xlabel('Trial', fontsize=AXIS_LABEL_SIZE, labelpad=AXIS_LABEL_PADDING)
    # Set the tick font size
    subplot.tick_params(labelsize=TICK_LABEL_SIZE, pad=TICK_LABEL_PADDING)
# Automatically generate a legend for the graph
fig.legend(fontsize=LEGEND_SIZE)
# Display the completed graph
plt.show()
