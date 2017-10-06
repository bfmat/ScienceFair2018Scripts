#!/usr/bin/env python

import os
import sys
import shutil


# A simple script to copy items in a folder into one of two subfolders,
# depending on whether they were created before or after a given time.
# Created by brendon-ai, September 2017


# Names of directories to move files into
SUBFOLDER_NAMES = ('before', 'after')


# Verify that the number of command line arguments is correct
if len(sys.argv) != 3:
    print('Usage: {} <image folder> <threshold Unix time>'.format(sys.argv[0]))
    sys.exit()

# Get a folder from the first command line argument
folder = os.path.expanduser(sys.argv[1])

# Get a Unix time value from the second argument
threshold_time = float(sys.argv[2])

# List for the full paths of the subfolders that will be created
subfolders = []

# Create a before directory and an after directory
for subfolder in SUBFOLDER_NAMES:

    # Format the full path
    subfolder_path = os.path.join(folder, subfolder)

    # Create the folder if it does not exist
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

    # Also add the folder's path to a list
    subfolders.append(subfolder_path)

# For each of the files in the main folder
for file_name in os.listdir(folder):

    # Format the file's full path
    file_path = os.path.join(folder, file_name)

    # If it is a file and not a folder
    if os.path.isfile(file_path):

        # If the file's modification time is lower than the provided time
        if os.path.getmtime(file_path) < threshold_time:

            # Copy the file to the before subfolder
            shutil.copy(file_path, subfolders[0])

        # Otherwise copy it to the after subfolder
        else:
            shutil.copy(file_path, subfolders[1])

