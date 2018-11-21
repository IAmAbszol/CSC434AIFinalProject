# Script to generate CSV of training inputs mapping to output

import numpy as np
import pandas as pd

# Create base input and labels
X = np.array([[1,0,0,0,0,0],
              [0,1,0,0,0,0],
              [1,1,0,0,0,0],
              [0,0,1,0,0,0],
              [0,0,0,1,0,0],
              [0,0,1,1,0,0],
              [1,0,0,0,1,0],
              [0,1,0,0,1,0],
              [1,1,0,0,1,0],
              [0,0,1,0,1,0],
              [0,0,0,1,1,0],
              [0,0,1,1,1,0]])

y = np.array([[0,1,1,1,0],
              [1,0,1,1,0],
              [0,0,1,1,0],
              [1,1,0,1,0],
              [1,1,1,0,0],
              [1,1,0,0,0],
              [0,0,1,1,0],
              [0,0,1,1,0],
              [0,0,1,1,0],
              [1,1,0,0,0],
              [1,1,0,0,0],
              [1,1,0,0,0]])

# Apply X and y through n iterations where n is max speed of car
max_speed = 10
X_append = X
y_append = y
for speed in range(1, max_speed + 1):
    X[:, 5] = speed
    X_append = np.append(X_append, X, axis=0)
    if speed == max_speed:
        y[:, 4] = 1
    y_append = np.append(y_append, y, axis=0)
