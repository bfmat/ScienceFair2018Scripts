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

# The number of X position steps used when calculating points on the polynomials for graphing
POLYNOMIAL_STEP_COUNT = 50

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

# Try to convert all of the elements to numbers, skipping empty lines with zero length
try:
    all_elements_numeric = [[int_or_float(element) for element in elements if len(element)]
                            for elements in all_elements]

# If it fails, print an error message and exit
except ValueError:
    print('Non-numeric or incorrectly formatted input.')
    sys.exit()

# If the lengths of the two lists are different, exit with an error message
if len(all_elements_numeric[0]) != len(all_elements_numeric[1]):
    print('Unequal number of', ATTRIBUTE_NAMES[0], 'points and', ATTRIBUTE_NAMES[1], 'points.')
    sys.exit()

# Prompt the user to enter the title of the graph
print('Enter the title of this graph.')
title = input()

# Set the title of the window
plt.figure('Test Data Graphing Tool')

# Set the title of the graph inside the window based on the user's input
plt.title(title)

# Plot a graph displaying the parameter and performance metric points, using square points
plt.plot(*all_elements_numeric, 's', label='Data points')

# Fit a line (degree 1) and a parabolic curve (degree 2) to the points
polynomials = [np.polyfit(*all_elements_numeric, deg=degree) for degree in [1, 2]]

# Get the first and last X positions of the data to use as outer bounds for the points on the polynomials
data_x_positions = all_elements_numeric[0]
min_x_position = min(data_x_positions)
max_x_position = max(data_x_positions)

# Calculate the step size to use based on the count and outer bounds
polynomial_step_size = (max_x_position - min_x_position) / POLYNOMIAL_STEP_COUNT

# Generate descriptions for the legend corresponding to the polynomials
descriptions = [name + ' of best fit' for name in ['Line', 'Parabola']]

# Iterate over the polynomials and corresponding descriptions
for polynomial, description in zip(polynomials, descriptions):

    # Reverse the array of polynomial parameters so that the lowest order comes first
    polynomial = np.flip(polynomial, 0)

    # List of X and Y positions on the current polynomial
    x_positions = []
    y_positions = []

    # Iterate over the X positions within the same range as the data, using the predefined step size
    for x_position in np.arange(min_x_position, max_x_position, polynomial_step_size):
        # For a polynomial of any order, calculate the Y position given the X position and polynomial parameters
        y_position = sum([(x_position ** order) * polynomial[order] for order in range(len(polynomial))])

        # Add both positions to their corresponding lists
        x_positions.append(x_position)
        y_positions.append(y_position)

    # Plot the points in this polynomial, and label it with the description
    plt.plot(x_positions, y_positions, label=description)

# Display a legend on the plot
plt.legend()

# Set the X and Y labels to the provided parameter and performance metric names
parameter_name, performance_metric_name = names
plt.xlabel(parameter_name)
plt.ylabel(performance_metric_name)

# Notify the user and show the graph
print('Opening the graph in a new window.')
plt.show()
