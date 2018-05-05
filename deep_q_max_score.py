#!/usr/bin/python3

import os
import sys

# Script to parse a log file produced by the new deep Q-network training system, outputting the maximum score, corresponding rolling average squared error and loss, episode number, and epsilon
# Created by brendon-ai, May 2018

# Verify that the number of command line arguments is correct
if len(sys.argv) != 2:
    print('Usage:', sys.argv[0], '<log file path>')
    sys.exit()

# Get the full path to the log file and read its contents
log_path = os.path.expanduser(sys.argv[1])
with open(log_path) as log_file:
    log_lines = log_file.readlines()

# Create a list to hold tuples of data from the file
data_tuples = []
# Iterate over the log's length, getting the words in the line containing the squared error and loss and also the index of the line containing the episode number, score, and epsilon
for error_line_index in range(len(log_lines) - 1):
    error_line_words = log_lines[error_line_index].split()
    episode_line_index = error_line_index + 1
    episode_line_words = log_lines[episode_line_index].split()
    # Verify that the current line and the next line are in the expected format; skip to the next iteration otherwise
    if error_line_words[0] != 'Over' or episode_line_words[0] != 'episode:':
        continue
    # Parse the rolling average squared error and loss
    squared_error = float(error_line_words[8])
    loss = float(error_line_words[13])
    # Parse the episode number, score, and epsilon
    episode = int(episode_line_words[1].split('/')[0])
    score = int(episode_line_words[3][:-1])
    epsilon = float(episode_line_words[5])
    # Package each of these values into a tuple and add it to the list
    data_tuples.append((squared_error, loss, episode, score, epsilon))

# Get the data corresponding to the maximum score and print it out
max_score_data_tuple = max(data_tuples, key=lambda data_tuple: data_tuple[3])
print('Squared error: {}, loss: {}, episode: {}, score, {}, epsilon: {}'
      .format(*max_score_data_tuple))
