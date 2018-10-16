import numpy as np


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
