#!/usr/bin/env python3

import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication

from automatic_cruise_control import automatic_cruise_control

# A visualization tool for the cruise control system that displays the environmental point map on screen and the
# calculated speed of the vehicle
# Created by brendon-ai, December 2017

# Height and width of the visualizer window
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 480


# Main PyQt5 QWidget class
class CruiseControlVisualizer(QWidget):
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
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle('Cruise Control Visualizer')
        # Display the window on screen
        self.show()

    # Update the user interface using data retrieved from the data thread
    def update_ui(self, data):
        # Unwrap the data tuple
        speed, samples = data
        print(speed)


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
