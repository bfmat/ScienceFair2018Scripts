from sweeppy import Sweep

# A script that handles slowing down the vehicle when close to another vehicle ahead, using the Sweep LIDAR sensor
# Created by brendon-ai, November 2017

# The file path to the LIDAR device
LIDAR_DEVICE_PATH = '/dev/cu.usbserial-DM00KERB'

# The number of millidegrees in a full rotation
FULL_ROTATION_ANGLE = 360 * 1000

# The angle in millidegrees away from the center within which a vehicle ahead is searched for
SEARCH_ANGLE = 10000

# The speed to travel at if there is no vehicle ahead within a certain range
DEFAULT_SPEED = 0.5

# The distance to the vehicle ahead at which the car begins to slow down
SLOW_RANGE = 1000

# The distance to the vehicle ahead at which the car stops completely
STOP_RANGE = 400


# Main generator that runs forever
def automatic_cruise_control():
    # Create a device using the constant path
    with Sweep(LIDAR_DEVICE_PATH) as sweep:
        # Use the maximum sample rate
        sweep.set_sample_rate(1000)

        # Start scanning with the Sweep sensor
        sweep.start_scanning()

        # Iterate over the data stream provided by the sensor
        for scan in sweep.get_scans():
            # Get the lowest distance to the car ahead within the predefined search angle of the center
            # Create an empty variable to store the lowest distance, starting at the maximum integer value
            closest_distance_within_search_angle = None

            # Iterate over the samples in the current scan
            for sample in scan.samples:

                # Get the distance and angle from the sample
                distance = sample.distance
                angle = sample.angle

                # If the sample's angle is within the permissible range in either direction
                if angle <= SEARCH_ANGLE or angle >= FULL_ROTATION_ANGLE - SEARCH_ANGLE:
                    # If either the distance has not been set or the current distance is less than the least one so far
                    if closest_distance_within_search_angle is None or distance < closest_distance_within_search_angle:
                        # If the distance is not 1 (that is, it is not infinite)
                        if distance != 1:
                            # Set the closest distance to the current one
                            closest_distance_within_search_angle = distance

            # If no points were found, return None
            if closest_distance_within_search_angle is None:
                yield (None,)
            # Otherwise, continue calculating the speed
            else:
                # If the distance to the car ahead is greater than the distance at which we need to go slowly
                # or it is 1 centimeter, which represents a distance larger than that which can be measured
                if closest_distance_within_search_angle > 500 or closest_distance_within_search_angle == 1:
                    # Set the speed to the default cruising speed
                    speed = DEFAULT_SPEED

                # If it is within the range at which is should stop
                elif closest_distance_within_search_angle <= STOP_RANGE:
                    # Set the speed to zero
                    speed = 0

                # Otherwise, the vehicle ahead is far enough away that we don't have to stop,
                # but close enough that we must slow down
                else:
                    # We need to linearly interpolate the speed between the cruising speed and zero
                    # Calculate how far we are away from having to stop
                    distance_past_stop_range = closest_distance_within_search_angle - STOP_RANGE

                    # Calculate the distance between the upper bound of the slow range and the stop range
                    # This is the range within which we will interpolate the speed
                    interpolation_range = SLOW_RANGE - STOP_RANGE

                    # Calculate the value by which we will interpolate by dividing the current distance past the stop
                    # range by the range between the upper bound of the stop range and the slow range
                    interpolation_value = distance_past_stop_range / interpolation_range

                    # Get the speed by multiplying the interpolation value by the default cruising speed
                    # This is equivalent to linear interpolation because the lower bound is always going to be zero
                    speed = interpolation_value * DEFAULT_SPEED

                # Yield the speed and the list of samples to whatever is iterating over this generator
                yield speed, closest_distance_within_search_angle, scan.samples
