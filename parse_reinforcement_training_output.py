#!/usr/bin/env python3


# A script for parsing the raw training output data files generated when training a reinforcement learning model, and
# calculating the average time on the road during the first 500 iterations


# The list that will contain the times before failure
times_before_failure = []

# For the first 500 lines
for _ in range(500):
    # Get the line passed as standard input (the file should be piped to this script)
    line = input()
    # Split the line by whitespace and parse element 3 (with the ending comma removed) as an integer
    # This is the time spent before failure
    time_before_failure = int(line.split()[3][:-1])
    # Add it to the list
    times_before_failure.append(time_before_failure)

# Print the mean of the list
print('Mean time before failure:', sum(times_before_failure) / len(times_before_failure))
