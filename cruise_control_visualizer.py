#!/usr/bin/env python3

import math
import sys

from PyQt5.QtCore import QThread, pyqtSignal, Qt, QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QApplication

from automatic_cruise_control import automatic_cruise_control

# A visualization tool for the cruise control system that displays the environmental point map on screen and the
# calculated speed of the vehicle
# Created by brendon-ai, December 2017

# Side length of the square visualizer window
WINDOW_SIDE_LENGTH = 600

# Scaling factor for mapping distances from the LIDAR sensor onto the screen, in pixels per centimeter
DISTANCE_SCALING_FACTOR = 0.5

# Diameter of the sample points drawn in the window
SAMPLE_POINT_DIAMETER = 3


# Main PyQt5 QWidget class
class CruiseControlVisualizer(QWidget):
    # List of points in the window corresponding to the samples collected by the LIDAR
    sample_points = []

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
                # On the circle centered at the origin with length of the distance multiplied by the scaling factor,
                # find the point corresponding to the angle
                # Do this with sine and cosine operations to calculate the corresponding point on the unit circle
                # and multiply that by the distance and the scaling factor
                # Finally, add half of the window's side length to center the points in the window
                sample_point = [
                    (trig_function(math.radians(sample.angle))
                     * sample.distance
                     * DISTANCE_SCALING_FACTOR)
                    + (WINDOW_SIDE_LENGTH / 2)
                    for trig_function in (math.cos, math.sin)
                ]
                # Add the point to the global list
                self.sample_points.append(sample_point)

        # Redraw the window
        self.repaint()

    # Called when the window is redrawn and used to display all of the sample points on the window
    def paintEvent(self, _):
        # Create a painter and begin painting
        painter = QPainter()
        painter.begin(self)
        # Paint the points in light gray with a light gray outline
        painter.setBrush(Qt.lightGray)
        painter.setPen(Qt.lightGray)

        # Iterate over the sample points
        for sample_point in self.sample_points:
            # Convert the tuple to a QPoint
            sample_qpoint = QPoint(*sample_point)
            # Draw the point on screen
            painter.drawEllipse(sample_qpoint, SAMPLE_POINT_DIAMETER, SAMPLE_POINT_DIAMETER)


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
