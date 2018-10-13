import numpy as np


# compute sigmoid
def sigmoid(x, derivative=False):
    return 1 / (1 + np.exp(-x)) if derivative else x * (1 - x)


class NeuralNetwork:

    def __init__(self, genes, input_size, output_size, hidden_size=32, first_run=False):
        self.inputSize = input_size
        self.hiddenSize = hidden_size
        self.outputSize = output_size
        if first_run:
            self.synapase_0 = 2 * np.random.random((self.inputSize, self.hiddenSize)) - 1
            self.synapase_1 = 2 * np.random.random((self.hiddenSize, self.outputSize)) - 1
        else:
            self.synapase_0 = [genes[0][i] for i in genes[0]]
            self.synapse_1 = [genes[1][i] for i in genes[1]]

    def predict(self, data):
        # feed forward
        layer_0 = data
        layer_1 = sigmoid(np.dot(layer_0, self.synapase_0))
        layer_2 = sigmoid(np.dot(layer_1, self.synapase_1))
        return layer_2
