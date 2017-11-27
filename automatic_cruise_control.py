#!/usr/bin/env python3

from sweeppy import Sweep

# A script that handles slowing down the vehicle when close to another vehicle ahead, using the Sweep LIDAR sensor
# Created by brendon-ai, November 2017

# The file path to the LIDAR device
LIDAR_DEVICE_PATH = '/dev/cu.usbserial-DM00KERB'

# The speed to travel at if there is no vehicle ahead within a certain range
DEFAULT_SPEED = 0.5

# The distance to the vehicle ahead at which the car begins to slow down
SLOW_RANGE = 1000

# The distance to the vehicle ahead at which the car stops completely
STOP_RANGE = 400

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

        # If the distance to the car ahead is greater than the distance at which we need to go slowly
        # or it is 1 centimeter, which represents a distance larger than that which can be measured
        if initial_distance > 500 or initial_distance == 1:
            # Set the speed to the default cruising speed
            speed = DEFAULT_SPEED

        # If it is within the range at which is should stop
        elif initial_distance <= STOP_RANGE:
            # Set the speed to zero
            speed = 0

        # Otherwise, the vehicle ahead is far enough away that we don't have to stop,
        # but close enough that we must slow down
        else:
            # We need to linearly interpolate the speed between the cruising speed and zero
            # Calculate how far we are away from having to stop
            distance_past_stop_range = initial_distance - STOP_RANGE

            # Calculate the distance between the upper bound of the slow range and the upper bound of the stop range
            # This is the range within which we will interpolate the speed
            interpolation_range = SLOW_RANGE - STOP_RANGE

            # Calculate the value by which we will interpolate by dividing the current distance past the stop range
            # by the range between the upper bound of the stop range and the slow range
            interpolation_value = distance_past_stop_range / interpolation_range

            # Get the speed by multiplying the interpolation value by the default cruising speed
            # This is equivalent to linear interpolation because the lower bound is always going to be zero
            speed = interpolation_value * DEFAULT_SPEED

        # Print the speed
        print(speed)
