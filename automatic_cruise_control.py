#!/usr/bin/env python3

from sweeppy import Sweep

# A script that handles slowing down the vehicle when close to another vehicle ahead, using the Sweep LIDAR sensor
# Created by brendon-ai, November 2017

# The file path to the LIDAR device
LIDAR_DEVICE_PATH = '/dev/cu.usbserial-DM00KERB'

# Create a device using the constant path
with Sweep(LIDAR_DEVICE_PATH) as sweep:
    # Use the maximum sample rate
    sweep.set_sample_rate(1000)

    # Start scanning with the Sweep sensor
    sweep.start_scanning()

    # Iterate over the data stream provided by the sensor
    for scan in sweep.get_scans():
        # Get the sample distance closest to the beginning of the rotation
        # The rotation starts and ends at the front of the sensor, opposite the cable
        initial_distance = scan.samples[0].distance

        # Output the distance to the terminal
        print(initial_distance)
