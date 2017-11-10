#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

# # A string that will be used as a termination character for multi-line inputs
# # Empty string represents an extra newline
# SENTINEL = ''
#
# # Lists to hold the names and lists of elements of the parameter and performance metric
# names = []
# all_elements = []
#
# # Prompt the user to enter the name and values of two attributes
# # One will be a parameter and the other is a performance metric
# for attribute_name in ['parameter', 'performance metric']:
#     # Prompt the user to enter the name of the parameter
#     print('Enter the name of the', attribute_name, 'to be plotted.')
#     name = input()
#
#     # Prompt the user to enter the list of values of the given parameter
#     print('Enter the values of the', attribute_name, 'with elements separated by newlines.')
#     print('End the list of values with two newlines in a row.')
#     elements = '\n'.join(iter(input, SENTINEL))
#
#     # Add the name and elements to corresponding lists
#     names.append(name)
#     all_elements.append(elements)
#
# # Strip whitespace from the names and elements
# names = [name.strip() for name in names]
# all_elements = [[element.strip() for element in elements] for elements in all_elements]
#
# # Convert all of the elements to floating-point numbers, skipping empty lines with zero length
# all_elements_numeric = [[float(element) for element in elements if len(element)] for elements in all_elements]

all_elements_numeric = [[-1.0, 1.0, 2.0, 3.0, 4.0], [41.8, 26.7, 10.5, 65.6, 80.2]]
names = ['Proportional multiplier', 'Standard deviation from center of road']

# Fit a line (degree 1) and a parabolic curve (degree 2) to the points
polynomials = [np.polyfit(*all_elements_numeric, deg=degree) for degree in [1, 2]]

# Plot a graph displaying the parameter and performance metric points
# Use red square points
plt.plot(*all_elements_numeric, 'rs')

# Set the X and Y labels to the provided parameter and performance metric names
parameter_name, performance_metric_name = names
plt.xlabel(parameter_name)
plt.ylabel(performance_metric_name)

# Show the graph
plt.show()
