from sweeppy import Sweep

# A script that handles slowing down the vehicle when close to another vehicle ahead, using the Sweep LIDAR sensor
# Created by brendon-ai, November 2017

# The file path to the LIDAR device
LIDAR_DEVICE_PATH = '/dev/cu.usbserial-DM00KERB'

# The number of millidegrees in a full rotation
FULL_ROTATION_ANGLE = 360 * 1000

# The angle in millidegrees away from the center within which a vehicle ahead is searched for
SEARCH_ANGLE = 10000

# The minimum distance in centimeters to the car ahead at which the vehicle will enable the accelerator
ACCELERATE_RANGE_CENTIMETERS = 40


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
                yield (None,) * 3
            # Otherwise, continue calculating the speed
            else:

                # If the closest distance is less than the predefined range, the vehicle should stop
                if closest_distance_within_search_angle < ACCELERATE_RANGE_CENTIMETERS:
                    accelerate = False
                # Otherwise, enable the accelerator
                else:
                    accelerate = True

                # Yield the speed and the list of samples to whatever is iterating over this generator
                yield accelerate, closest_distance_within_search_angle, scan.samples
