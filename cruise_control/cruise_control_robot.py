#!/usr/bin/env python3

import sys

import paramiko

from cruise_control.cruise_control_loop import automatic_cruise_control

# A script to run the cruise control loop and allow it to interface with the robot code running on the roboRIO
# Created by brendon-ai, December 2017

# Create an SSH client
ssh_client = paramiko.SSHClient()
# Load host keys from the system SSH
ssh_client.load_system_host_keys()
# Try to connect to the roboRIO
try:
    ssh_client.connect(
        hostname='192.168.0.230',
        username='lvuser',
        password=''
    )
# If an error is thrown
except (paramiko.ssh_exception.SSHException, EOFError):
    # Print an error and exit
    sys.exit('Failed to connect to the roboRIO')

# Iterate over the cruise control loop
for accelerate, _, _ in automatic_cruise_control():
    # Run the command to write the acceleration value to a file on the roboRIO
    ssh_client.exec_command('echo {} > /home/lvuser/lidar.dat'.format(accelerate))
