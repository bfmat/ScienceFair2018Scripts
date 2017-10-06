#!/usr/bin/env python

import os
import sys


# A script to calculate the average time between frames of a dataset based on Unix timestamps
# Created by brendon-ai, October 2017

# Verify that the number of command line arguments is correct
if len(sys.argv) != 2:
    print('Usage: {} <image folder>')

# Iterate over the files in the folder
image_folder = os.path.expanduser(sys.argv[1])
for file_name in os.listdir(image_folder):
