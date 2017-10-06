#!/usr/bin/env python

from __future__ import print_function

import os
import sys


# A script to calculate the average time between frames of a dataset based on Unix timestamps
# Created by brendon-ai, October 2017


# Verify that the number of command line arguments is correct
if len(sys.argv) != 2:
    print('Usage: {} <image folder>'.format(sys.argv[0]))
    sys.exit()

# Iterate over the files in the folder and get a list of their timestamps
image_folder = os.path.expanduser(sys.argv[1])
timestamps = [os.path.getmtime('{}/{}'.format(image_folder, file_name)) for file_name in os.listdir(image_folder)]

# Sort the list of timestamps, skipping the first element because it is the initial value of the previous timestamp
timestamps_sorted = sorted(timestamps[1:])

# Add up the time deltas while iterating
total_delta_time = 0

# Previous timestamp is used to calculate the delta between timestamp X and timestamp X - 1
previous_timestamp = timestamps_sorted[0]

# Iterate over the sorted timestamps
for timestamp in timestamps_sorted:

    # Calculate the delta between the current timestamp and the last and add it to the total
    delta_time = timestamp - previous_timestamp
    total_delta_time += delta_time

    # Set the previous timestamp
    previous_timestamp = timestamp

# Calculate the average of the time deltas and print the results
num_iterations = len(timestamps_sorted)
average_delta_time = total_delta_time / num_iterations
print('Average delta over', num_iterations, 'iterations:', average_delta_time)
