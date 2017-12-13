#!/usr/bin/env python3

import math
import sys

from PyQt5.QtCore import QThread, pyqtSignal, Qt, QPoint, QPointF
from PyQt5.QtGui import QColor, QPainter, QPalette, QPolygon
from PyQt5.QtWidgets import QWidget, QApplication

from cruise_control.automatic_cruise_control import automatic_cruise_control, SEARCH_ANGLE

# A visualization tool for the cruise control system that displays the environmental point map on screen and the
# calculated speed of the vehicle
# Created by brendon-ai, December 2017

# Side length of the square visualizer window
WINDOW_SIDE_LENGTH = 700

# Scaling factor for mapping distances from the LIDAR sensor onto the screen, in pixels per centimeter
DISTANCE_SCALING_FACTOR = 0.05

# Diameter of the sample points drawn in the window
SAMPLE_POINT_DIAMETER = 3


# Main PyQt5 QWidget class
class CruiseControlVisualizer(QWidget):
    # List of points in the window corresponding to the samples collected by the LIDAR
    sample_points = []

    # The triangle that will be displayed on screen to mark the edges of the search range
    triangle = None

    # Prepare the UI and data thread and run the main loop
    def __init__(self):
        # Call the QWidget initializer
        super(CruiseControlVisualizer, self).__init__()

        # Create an instance of the data thread that takes information from the LIDAR in the background
        data_thread = CruiseControlVisualizerDataThread()
        # Connect the data signal to the UI update function in the main thread
        data_thread.data_signal.connect(self.update_ui)
        # Start the data thread
        data_thread.start()

        # Initialize the user interface
        self.init_ui()

    # Create the window and all elements within it
    def init_ui(self):
        # Set the window's size and title
        self.setFixedSize(WINDOW_SIDE_LENGTH, WINDOW_SIDE_LENGTH)
        self.setWindowTitle('Cruise Control Visualizer')
        # Use a dark blue background
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(0x000040))
        self.setPalette(palette)

        # Create a gray triangle with one vertex at the center of the window and the two sides that intersect at this
        # vertex each angled at the edges of the search range for the vehicle ahead
        # Start by calculating the points described above using simple trigonometry and creating a triangle
        # The first vertex should be in the exact center of the image
        center_dimension = WINDOW_SIDE_LENGTH / 2
        center_point = QPoint(center_dimension, center_dimension)
        # Create a list of vertices for the triangle initially containing only the center point
        triangle_vertices = [center_point]
        # Calculate a point for both edges of the search range
        for side_angle in (-SEARCH_ANGLE, SEARCH_ANGLE):
            # Convert the angle to a point on the unit circle
            unit_circle_point = self.angle_to_point_on_unit_circle(side_angle)
            # Convert the tuple to a QPointF
            unit_circle_qpointf = QPointF(*unit_circle_point)
            # Multiply the unit circle vector by the width of the window to get a vector that will reach outside of the
            # window, and add the center point to it to ensure that they radiate out from the center of the window
            # Also convert it to an integer QPoint instead of a floating-point QPointF
            triangle_vertex = ((unit_circle_qpointf * WINDOW_SIDE_LENGTH) + center_point).toPoint()
            # Add it to the list of vertices
            triangle_vertices.append(triangle_vertex)
        # Create a polygon out of the vertices
        self.triangle = QPolygon(triangle_vertices)

        # Display the window on screen
        self.show()
        self.update_ui((None, None))

    # Update the user interface using data retrieved from the data thread
    def update_ui(self, data):
        # Clear the global list of sample points
        self.sample_points = []

        # Unwrap the data tuple
        speed, samples = data
        # If there is a valid list of samples
        if samples is not None:
            # Iterate over the samples
            for sample in samples:
                # Convert the angle in the sample to a vector on the unit circle
                unit_circle_vector = self.angle_to_point_on_unit_circle(sample.angle)
                # Scale the vector so that it is the same length as the distance of the sample, convert its elements
                # to integers, and make it into a QPoint
                scaled_vector_integer = [int(round(dimension * sample.distance)) for dimension in unit_circle_vector]
                scaled_vector_qpoint = QPoint(*scaled_vector_integer)
                # Offset the point so that its origin is halfway across the window in both dimensions
                half_window_side_length = WINDOW_SIDE_LENGTH / 2
                sample_point = scaled_vector_qpoint + (QPoint(half_window_side_length, half_window_side_length))
                # Add the point to the global list
                self.sample_points.append(sample_point)

        # Redraw the window
        self.repaint()

    # Called when the window is redrawn and used to display all of the sample points on the window
    def paintEvent(self, _):

        # Create a painter and begin painting
        painter = QPainter()
        painter.begin(self)

        # Draw the search range triangle with a gray fill and a light gray outline
        painter.setBrush(Qt.gray)
        painter.setPen(Qt.lightGray)
        painter.drawPolygon(self.triangle)

        # Paint the sample points in light gray with a light gray outline
        painter.setBrush(Qt.lightGray)
        painter.setPen(Qt.lightGray)
        # Iterate over the sample points and draw them
        for sample_point in self.sample_points:
            # Draw the point on screen
            painter.drawEllipse(sample_point, SAMPLE_POINT_DIAMETER, SAMPLE_POINT_DIAMETER)

        # Stop painting
        painter.end()

    # A function to convert an angle in millidegrees to a corresponding point on the unit circle
    @staticmethod
    def angle_to_point_on_unit_circle(angle_millidegrees):
        # Convert the angle from millidegrees to radians
        side_angle_radians = math.radians(angle_millidegrees / 1000)
        # Calculate the point corresponding to this angle on the unit circle using simple trigonometric functions
        # It will be formatted as a list since it is being calculated in a list comprehension
        point_as_list = [trig_function(side_angle_radians)
                         for trig_function in (math.sin, lambda x: -math.cos(x))]
        # Convert the list to a tuple and return it
        return tuple(point_as_list)


# The data thread that runs forever, accepting values from the LIDAR and displaying them on screen
class CruiseControlVisualizerDataThread(QThread):
    # The signal that is called when it is time to transfer data to the main thread
    data_signal = pyqtSignal(tuple)

    # Initializer containing nothing but a call to the QThread initializer
    def __init__(self):
        QThread.__init__(self)

    # The function containing the logic of the main loop
    def run(self):
        # Iterate over the automatic cruise control generator
        for data in automatic_cruise_control():
            # Send the speed and samples through the signal to the UI thread
            self.data_signal.emit(data)


# If this file is being run directly, instantiate the ManualSelection class
if __name__ == '__main__':
    app = QApplication([])
    ic = CruiseControlVisualizer()
    sys.exit(app.exec_())
