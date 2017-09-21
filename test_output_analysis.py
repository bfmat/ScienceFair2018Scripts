#!/usr/bin/env python

from __future__ import print_function

import os
import sys
import math


# A script for calculating the standard deviation from the center of the road
# for a set of images generated during real-world testing.
# Created by brendon-ai, September 2017


# Check that the number of command line arguments is correct
if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<image folder>')
    sys.exit()

# Parse the provided folder path
folder = os.path.expanduser(sys.argv[1])

# Accumulate the total squared errors for all of the files
total_squared_error = 0.

# Iterate over all of the image names in the folder
file_names = os.listdir(folder)
for file_name in file_names:

    # Get the part of the file name after the word 'error'
    file_name_end = file_name.split('error')[1]

    # The error is the part of the remaining name before the first period
    error = int(file_name_end.split('.')[0])

    # Add the square of the error to the accumulator
    total_squared_error += error ** 2

# Save the number of files there are
num_files = len(file_names)

# Calculate the standard deviation from the total squared error
variance = total_squared_error / num_files
standard_deviation = math.sqrt(variance)

# Print the results
print('Standard deviation over', num_files, 'images:', standard_deviation)
