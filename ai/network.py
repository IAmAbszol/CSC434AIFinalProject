import numpy as np
import tensorflow as tf

from sklearn import model_selection

# compute sigmoid
def sigmoid(x, derivative=False):
    return 1 / (1 + np.exp(-x)) if derivative else x * (1 - x)

class NeuralNetwork:

    def __init__(self, genes, input_size, hidden_size, output_size):
        self.inputSize = input_size
        self.hiddenSize = hidden_size
        self.outputSize = output_size
        self.synapse_0 = np.reshape(genes[:(input_size * hidden_size)], (-1, hidden_size))
        self.synapse_1 = np.reshape(genes[(input_size * hidden_size):(input_size * hidden_size) + (hidden_size * output_size)], (-1, output_size))


    def predict(self, data):
        # feed forward
        layer_0 = data
        layer_1 = sigmoid(np.dot(layer_0, self.synapse_0))
        layer_2 = sigmoid(np.dot(layer_1, self.synapse_1))
        return layer_2

    def train(self):
        # Create base input and labels
        X = np.array([[1, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0],
                      [1, 1, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0],
                      [0, 0, 1, 1, 0, 0],
                      [1, 0, 0, 0, 1, 0],
                      [0, 1, 0, 0, 1, 0],
                      [1, 1, 0, 0, 1, 0],
                      [0, 0, 1, 0, 1, 0],
                      [0, 0, 0, 1, 1, 0],
                      [0, 0, 1, 1, 1, 0]])

        y = np.array([[0, 1, 1, 1, 0],
                      [1, 0, 1, 1, 0],
                      [0, 0, 1, 1, 0],
                      [1, 1, 0, 1, 0],
                      [1, 1, 1, 0, 0],
                      [1, 1, 0, 0, 0],
                      [0, 0, 1, 1, 0],
                      [0, 0, 1, 1, 0],
                      [0, 0, 1, 1, 0],
                      [1, 1, 0, 0, 0],
                      [1, 1, 0, 0, 0],
                      [1, 1, 0, 0, 0]])

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

        X = X_append
        y = y_append

        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=.2, random_state=5)

        # View professor yu's labs.
        # Use tensorflow for feed forward/backward prop adjustment
        # and to collect the weights. Apply same for the predict
        # Want to use y = wx + b