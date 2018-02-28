#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd

# A tool for graphing changing characteristics over a series of trials
# Created by brendon-ai, February 2018

# Get the number of trials, and the number of data series per trial, from the user
num_trials = int(input('Enter the number of trials: '))
num_series = 2 if input('Enter "y" if two data series are being used: ') == 'y' else 1
# Get the names of the trials
print('Enter the names of the {} trials, each on a separate line:'.format(num_trials))
trial_names = [input().strip() for _ in range(num_trials)]

# The width to make the bars for a single trial
bar_width = 0.4
# Make the bars half as wide if there is only one series
if num_series == 1:
    bar_width /= 2
# Create a figure and add a subplot, duplicating its X axis into a different plot if there are two series
fig = plt.figure()
subplots = [fig.add_subplot(111)]
if num_series == 2:
    subplots.append(subplots[0].twinx())

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
print(data_frame)
