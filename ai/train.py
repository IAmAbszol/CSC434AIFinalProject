# Script to generate CSV of training inputs mapping to output

import numpy as np
import tensorflow as tf
import itertools
import time

from sklearn import model_selection

# Create base input and labels
X = np.zeros(shape=(1, 5))
for i in itertools.product([0, 1], repeat=4):
    X = np.append(X, [np.append(np.array(i), 0)], axis=0)
X = np.delete(X, (0), axis=0)

y_label = np.zeros(shape=(1, 5))
for row in X:
    y_label_list = []
    for index, element in enumerate(row):
        if index == 4:
            y_label_list.append(0)
            y_label = np.append(y_label, [y_label_list], axis=0)
            break
        if element == 0:
            y_label_list.append(1)
        else:
            y_label_list.append(0)
y_label = np.delete(y_label, (0), axis=0)

# Set max speed, the car can go to a max but
# that doesn't mean it should.
X_tmp = X
y_label_tmp = y_label
for speed in range(1, 8 + 1):
    X_tmp[:, -1] = speed
    X = np.append(X, X_tmp, axis=0)
    if speed == 8:
        y_label_tmp[:, :] = 0
        y_label_tmp[:, -1] = 1
    else:
        y_label_tmp[:, -1] = 0
    y_label = np.append(y_label, y_label_tmp, axis=0)

# Create multiple large duplicates of the data
X = np.repeat(X, 25, axis=0)
y_label = np.repeat(y_label, 25, axis=0)

# Train network and obtain weights
input_layer = X.shape[1]
hidden_layer = 32
output_layer = y_label.shape[1]
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y_label, test_size=.2, random_state=5)

X_data = tf.placeholder(tf.float32, shape=[None, input_layer], name='x-inputdata')
y_target = tf.placeholder(tf.float32, shape=[None, output_layer], name='y-targetdata')

weight_one = tf.Variable(tf.random_uniform([input_layer, hidden_layer], -1, 1), name="Weight_One")
weight_two = tf.Variable(tf.random_uniform([hidden_layer, output_layer], -1, 1), name="Weight_Two")

bias_one = tf.Variable(tf.zeros([hidden_layer]), name="Bias_One")
bias_two = tf.Variable(tf.zeros([output_layer]), name="Bias_Two")

with tf.name_scope("layer2") as scope:
    synapse0 = tf.sigmoid(tf.matmul(X_data, weight_one) + bias_one, name="Synapse0")

with tf.name_scope("layer3") as scope:
    hypothesis = tf.sigmoid(tf.matmul(synapse0, weight_two) + bias_two, name="Hypothesis")

with tf.name_scope("cost") as scope:
    cost = tf.reduce_mean(((y_target * tf.log(hypothesis)) + ((1 - y_target) * tf.log(1.0 - hypothesis))) * -1,
                          name="Cost")

# Rationale behind GDO can be found on iamtrask NN
with tf.name_scope("train") as scope:
    train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cost)

init = tf.global_variables_initializer()

saver = tf.train.Saver()

with tf.Session() as sess:

    writer = tf.summary.FileWriter("../summary_train", sess.graph)

    sess.run(init)

    t_start = time.clock()
    for i in range(100000):
        sess.run(train_step, feed_dict={X_data: X_train, y_target: y_train})
        if i % 1000 == 0:
            print("Epoch ", i)
            print("Hypothesis ", sess.run(hypothesis, feed_dict={X_data: X_train, y_target: y_train}))
            print("Weight 1 ", sess.run(weight_one))
            print("Bias 1 ", sess.run(bias_one))
            print("Weight 2 ", sess.run(weight_two))
            print("Bias 2 ", sess.run(bias_two))
            print("cost ", sess.run(cost, feed_dict={X_data: X_train, y_target: y_train}))
    t_end = time.clock()
    print("Elapsed time ", (t_end - t_start))

    # Save to output due to training being complete
    save_path = saver.save(sess, "./models/pretrained_car.ckpt")
    writer.close()

    print("Testing logic operators.")
    for i in range(len(X_test)):
        print("Input {} --> Actual {}, Predicted {}".format(X_test[i], y_test[i], np.rint(sess.run(hypothesis, feed_dict={X_data: [X_test[i]]}))))

