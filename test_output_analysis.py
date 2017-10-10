#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import math


# A script for analyzing output data from an autonomous vehicle, including calculating the standard deviation from the
# road line based on the file names, the average time elapsed per frame based on the timestamps of the files, and
# calculating the geometric mean of the derivative of the error, which provides information on unwanted oscillation


# Check that the number of command line arguments is correct
if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<image folder>')
    sys.exit()


# First, get all of the timestamps and errors from the file names and metadata
# Parse the provided folder path
folder = os.path.expanduser(sys.argv[1])

# Gather a list of timestamps and a list of errors for later processing
timestamps = []
errors = []

# Iterate over all of the image names in the folder
file_names = os.listdir(folder)
for file_name in file_names:

    # Get the part of the file name after the word 'error'
    file_name_end = file_name.split('error')[1]

    # The error is the part of the remaining name before the first period
    error = int(file_name_end.split('.')[0])

    # Add it to the list
    errors.append(error)

    # Get the timestamp of the file and add it to the list
    timestamp = os.path.getmtime('{}/{}'.format(folder, file_name))
    timestamps.append(timestamp)


# Next task is to compute the average frame time and geometric mean of the approximate derivative of the error
# Sort the timestamps so they are iterated over, and keep them in order with the corresponding errors
timestamps_with_errors = zip(timestamps, errors)
timestamps_with_errors_sorted = sorted(timestamps_with_errors, key=lambda timestamp_and_error: timestamp_and_error[0])

# Split them into two lists once again
timestamps_with_errors_unzipped = list(zip(*timestamps_with_errors_sorted))
timestamps_sorted = timestamps_with_errors_unzipped[0]
errors_sorted = timestamps_with_errors_unzipped[1]

# Add up the time deltas and the squared derivatives while iterating
total_delta_time = 0
total_squared_derivative_error = 0

# Iterate over the sorted timestamps and errors
for i in range(1, len(timestamps_with_errors_sorted)):

    # Get the indices for the current iteration and the previous one
    current_iteration = i
    previous_iteration = i - 1

    # Calculate the delta between the current timestamp and the last and add it to the total
    delta_time = timestamps_sorted[current_iteration] - timestamps_sorted[previous_iteration]
    total_delta_time += delta_time

    # Calculate the approximate derivative of the error with respect to time at this point
    delta_error = errors_sorted[current_iteration] - errors_sorted[previous_iteration]
    derivative_error = delta_error / delta_time

    # Add the square of the derivative to the total
    squared_derivative_error = derivative_error ** 2
    total_squared_derivative_error += squared_derivative_error


# Perform final calculations and print out all of the results
# Get the number of files there are in the list and the number of iterations involved in the derivative calculation
num_files = len(file_names)
num_iterations = num_files - 1

# Calculate and print the average frame time
average_frame_time = total_delta_time / num_iterations
print('Average frame time over', num_iterations, 'iterations:', average_frame_time)

# Calculate and print the standard deviation from the total squared error
total_squared_error = sum([error ** 2 for error in errors])
error_variance = total_squared_error / num_files
error_standard_deviation = math.sqrt(error_variance)
print('Standard deviation from predicted center line over', num_files, 'images:', error_standard_deviation)

# Calculate and print the geometric mean of the total squared error derivative
derivative_error_variance = total_squared_derivative_error / num_iterations
derivative_error_geometric_mean = math.sqrt(derivative_error_variance)
print('Geometric mean of approximate derivative of error from predicted center line over',
      num_iterations, 'iterations:', derivative_error_geometric_mean)
