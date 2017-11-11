#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import numpy as np


# A function to convert a string to an integer, and if it fails, then convert it to a float instead
def int_or_float(string):
    try:
        return int(string)
    except ValueError:
        return float(string)


# Descriptions for the general concepts of the two attributes of the graph
ATTRIBUTE_NAMES = ['parameter', 'performance metric']

# The X position step size used when calculating points on the polynomials for graphing
POLYNOMIAL_STEP_SIZE = 0.05

# Lists to hold the names and lists of elements of the parameter and performance metric
names = []
all_elements = []

# Prompt the user to enter the name and values of two attributes
for attribute_name in ATTRIBUTE_NAMES:
    # Prompt the user to enter the name of the parameter
    print('Enter the name of the', attribute_name, 'to be plotted.')
    name = input()

    # Prompt the user to enter the list of values of the given parameter
    print('Enter the values of the', attribute_name, 'with elements separated by newlines.')
    print('End the list of values with a newline followed by an end-of-file character (control-D).')
    elements = sys.stdin.readlines()

    # Add the name and elements to corresponding lists
    names.append(name)
    all_elements.append(elements)

# Strip whitespace from the names and elements
names = [name.strip() for name in names]
all_elements = [[element.strip() for element in elements] for elements in all_elements]

# Convert all of the elements to numbers, skipping empty lines with zero length
all_elements_numeric = [[int_or_float(element) for element in elements if len(element)] for elements in all_elements]

# If the lengths of the two lists are different, exit with an error message
if len(all_elements_numeric[0]) != len(all_elements_numeric[1]):
    print('Unequal number of', ATTRIBUTE_NAMES[0], 'points and', ATTRIBUTE_NAMES[1], 'points.')
    sys.exit()

# Plot a graph displaying the parameter and performance metric points, using square points
plt.plot(*all_elements_numeric, 's')

# Fit a line (degree 1) and a parabolic curve (degree 2) to the points
polynomials = [np.polyfit(*all_elements_numeric, deg=degree) for degree in [1, 2]]

# Get the first and last X positions of the data to use as outer bounds for the points on the polynomials
data_x_positions = all_elements_numeric[0]
first_x_position = data_x_positions[0]
last_x_position = data_x_positions[-1]

# Iterate over the polynomials
for polynomial in polynomials:

    # Reverse the array of polynomial parameters so that the lowest order comes first
    polynomial = np.flip(polynomial, 0)

    # List of X and Y positions on the current polynomial
    x_positions = []
    y_positions = []

    # Iterate over the X positions within the same range as the data, using the predefined step size
    for x_position in np.arange(first_x_position, last_x_position, POLYNOMIAL_STEP_SIZE):
        # For a polynomial of any order, calculate the Y position given the X position and polynomial parameters
        y_position = sum([(x_position ** order) * polynomial[order] for order in range(len(polynomial))])

        # Add both positions to their corresponding lists
        x_positions.append(x_position)
        y_positions.append(y_position)

    # Plot the points in this polynomial
    plt.plot(x_positions, y_positions)

# Set the X and Y labels to the provided parameter and performance metric names
parameter_name, performance_metric_name = names
plt.xlabel(parameter_name)
plt.ylabel(performance_metric_name)

# Notify the user and show the graph
print('Opening the graph in a new window.')
plt.show()
