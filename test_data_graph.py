#!/usr/bin/env python3

import matplotlib.pyplot as plt

# A string that will be used as a termination character for multi-line inputs
# Empty string represents an extra newline
SENTINEL = ''

# Lists to hold the names and lists of elements of the parameter and performance metric
names = []
all_elements = []

# Prompt the user to enter the name and values of two attributes
# One will be a parameter and the other is a performance metric
for attribute_name in ['parameter', 'performance metric']:
    # Prompt the user to enter the name of the parameter
    print('Enter the name of the', attribute_name, 'to be plotted.')
    name = input()

    # Prompt the user to enter the list of values of the given parameter
    print('Enter the values of the', attribute_name, 'with elements separated by newlines.')
    print('End the list of values with two newlines in a row.')
    elements = '\n'.join(iter(input, SENTINEL))

    # Add the name and elements to corresponding lists
    names.append(name)
    all_elements.append(elements)

# Strip whitespace from the names and elements
names = [name.strip() for name in names]
all_elements = [[element.strip() for element in elements] for elements in all_elements]

# Convert all of the elements to floating-point numbers, skipping empty lines with zero length
all_elements_numeric = [[float(element) for element in elements if len(element)] for elements in all_elements]

# Plot a graph displaying the parameter and performance metric points
plt.plot(*all_elements_numeric)

# Show the graph
plt.show()
