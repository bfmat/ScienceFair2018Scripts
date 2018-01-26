#!/bin/sh

# A script for running all of the required elements for driving in the simulation and finding stop signs
# Created by brendon-ai, January 2018

# Go to the root folder of all of my scripts
cd ~/Developer

# Run the driving script in the background (the path is hardcoded for my system)
python2 -m LaneDetection.apply.simulation_stream \
~/Developer/Models/TrainedModels/batch=1513889469-epoch=10-val_loss=0.086984.h5 &

# Run the stop sign finding script in the foreground
python3 -m StopSignFinder.infer ~/Developer/Models/StopSignModels/TrainedWithNegative.h5

# When the foreground process is interrupted, kill the background process
pkill Python
