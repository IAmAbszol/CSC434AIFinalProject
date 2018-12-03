import numpy as np
import tensorflow as tf

from sklearn import model_selection

# compute sigmoid
def sigmoid(x, derivative=False):
    return 1 / (1 + np.exp(-x)) if derivative else x * (1 - x)

class NeuralNetwork:

    def __init__(self, w1, b1, w2, b2, input_layer, output_layer):
        w1_np = np.asarray(w1, np.float32)
        b1_np = np.asarray(b1, np.float32)
        w2_np = np.asarray(w2, np.float32)
        b2_np = np.asarray(b2, np.float32)

        w1_tf = tf.convert_to_tensor(w1_np, np.float32)
        b1_tf = tf.convert_to_tensor(b1_np, np.float32)
        w2_tf = tf.convert_to_tensor(w2_np, np.float32)
        b2_tf = tf.convert_to_tensor(b2_np, np.float32)

        self.X_data = tf.placeholder(tf.float32, shape=[None, input_layer], name='x-inputdata')

        weight_one = w1_tf
        weight_one = tf.identity(weight_one, name="Weight_One")
        weight_two = w2_tf
        weight_two = tf.identity(weight_two, name="Weight_Two")

        bias_one = b1_tf
        bias_one = tf.identity(bias_one, name="Bias_One")
        bias_two = b2_tf
        bias_two = tf.identity(bias_two, name="Bias_Two")

        with tf.name_scope("layer2") as scope:
            synapse0 = tf.sigmoid(tf.matmul(self.X_data, weight_one) + bias_one, name="Synapse0")

        with tf.name_scope("layer3") as scope:
            self.hypothesis = tf.sigmoid(tf.matmul(synapse0, weight_two) + bias_two, name="Hypothesis")

        self.init = tf.global_variables_initializer()

        self.sess = tf.Session()
        self.sess.run(self.init)

    def predict(self, data):

            return self.sess.run(self.hypothesis, feed_dict={self.X_data : [data]})