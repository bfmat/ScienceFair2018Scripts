#!/usr/bin/env python3

import sys

from PyQt5.QtWidgets import QWidget, QApplication

from automatic_cruise_control import automatic_cruise_control


# A visualization tool for the cruise control system that displays the environmental point map on screen and the
# calculated speed of the vehicle
# Created by brendon-ai, December 2017

# Main PyQt5 QWidget class
class CruiseControlVisualizer(QWidget):

    # Prepare the UI and run the main loop
    def __init__(self):
        # Call the QWidget initializer
        super(CruiseControlVisualizer, self).__init__()

        # Initialize the user interface
        self.init_ui()
        # Start the main loop
        self.main_loop()

    # Create the window and all elements within it
    def init_ui(self):
        # Display the window on screen
        self.show()

    # Run forever, accepting values from the LIDAR and displaying them on screen
    def main_loop(self):
        # Iterate over the automatic cruise control generator
        for speed, samples in automatic_cruise_control():
            print(speed)


# If this file is being run directly, instantiate the ManualSelection class
if __name__ == '__main__':
    app = QApplication([])
    ic = CruiseControlVisualizer()
    sys.exit(app.exec_())
