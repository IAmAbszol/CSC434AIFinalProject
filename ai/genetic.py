"""
genetic.py
-----------

Parameters for the Genes are
1. Hyper-parameter tuple of synapse 0
2. Hyper-parameter tuple of synapse 1
"""

import pygame
import math
import datetime
import random
import os
import numpy as np
from bisect import bisect_left
import sys, os
from ai import network
import tensorflow as tf

OPTIMIZER = 0
INPUT = 4
HIDDEN = 12
OUTPUT = 6


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def euclidean(dx, dy):
    return np.sqrt((dx[1] - dx[0]) ** 2 + (dy[1] - dy[0]) ** 2)


class GeneticAlgorithm:

    def __init__(self, pool_size=10):

        try:
            os.remove("log.txt")
        except OSError:
            pass

        self.pool = pool_size
        self.crossover_pool = 25
        self.first_run = True
        self.parent = self.bestParent = None
        self.strategy_pool = ["Create", "Mutate", "Crossover"]
        # takes ~13 seconds on testing system. Called once per class creation
        self.Geneset = list(frange(-5, 5, .000001))
        self.loaded_model = False
        self.w1, self.b1, self.w2, self.b2 = self.load()
        self.Genelength = OPTIMIZER + len(self.numpytolinear((self.w1, self.b1, self.w2, self.b2)))
        self.maxAge = 5
        self.startTime = 0
        self.parents = []
        self.historicalFitnesses = []
        self.lastParentIndex = (self.crossover_pool - 1) if self.crossover_pool < pool_size else (pool_size - 1)
        self.pIndex = 1

    def _display(self, candidate):
        file = open("log.txt", "a")
        file.write("Fitness: {} - Strategy: {} - {} - Genes: {}\n".format(candidate.Fitness, candidate.Strategy,
                                                                          (datetime.datetime.now() - self.startTime),
                                                                          candidate.Genes))
        file.close()

    def _crossover(self, participant_a, participant_b):
        child = self.Chromosome(0, 0, "Crossover")
        childGenes = []
        for i in range(len(participant_a.Genes)):
            if random.uniform(0, 1) > 0.5:
                childGenes.append(participant_b.Genes[i])
            else:
                childGenes.append((participant_a.Genes[i]))
        child.Genes = childGenes
        return child

    def _mutate(self, participant, geneset):
        child = self.Chromosome(0, 0, "Mutate")
        childGenes = tmpGenes = participant.Genes[:]
        for gene in range(len(tmpGenes)):
            tmpGenes[gene] = geneset[random.randrange(0, len(geneset))]
        for i in range(0, len(childGenes)):
            if random.uniform(0, 1) > 0.6:
                childGenes[i] = tmpGenes[i]
        child.Genes = childGenes
        return child

    def _create(self, length, geneset):
        if self.loaded_model:
            self.loaded_model = False
            participant = self.Chromosome(np.append(np.array([1 for i in range(OPTIMIZER)]),
                                                    self.numpytolinear((self.w1, self.b1, self.w2, self.b2))), 0,
                                          "Create")
        else:
            participant = self.Chromosome([i for i in range(length)], 0, "Create")
            for i in range(length):
                participant.Genes[i] = geneset[random.randrange(0, len(geneset))]
        return participant

    def construct_cars(self, car_pos):
        if self.first_run:
            for i in range(self.pool):
                yield self.CarSprite(self, "images/car.png", car_pos, self._create(self.Genelength, self.Geneset))
        else:
            for i in range(self.pool):
                strategy = random.choice(self.strategy_pool)
                if strategy is "Create":
                    yield self.CarSprite(self, "images/car.png", car_pos, self._create(self.Genelength, self.Geneset))
                elif strategy is "Mutate":
                    yield self.CarSprite(self, "images/car.png", car_pos, self._mutate(self.parent, self.Geneset))
                elif strategy is "Crossover":
                    yield self.CarSprite(self, "images/car.png", car_pos, self._mutate(self._crossover(
                        self.parents[random.randrange(0, len(self.parents))],
                        self.parents[random.randrange(0, len(self.parents))]), self.Geneset))

    # parameters required such as distance, etc. Possibly capture within car?
    def get_fitness(self, participants, data, car=True):
        if car:
            for index, participant in enumerate(participants):
                if participant.distance > 0:
                    participant.Chromosome.Fitness = len(
                        set(list(zip([history.X for history in participant.history],
                                     [history.Y for history in participant.history]))))
									 
                if participant.win:
                    participant.Chromosome.Fitness += 10000
        else:
            participants.Fitness = 0
        return participants

    def evaluate_performance(self, participants, data):
        participants = self.get_fitness(participants, data)
        participants_genes = [i.Chromosome for i in participants]
        sorted_participants = sorted(participants_genes, reverse=True)
        if self.first_run:
            self.startTime = datetime.datetime.now()
            self.bestParent = self._create(self.Genelength, self.Geneset)
            self.parents = [self.bestParent]
            self.historicalFitnesses = [self.bestParent.Fitness]

            # evaluate first run candidates/participants
            for _ in range(self.crossover_pool - 1):
                if _ < len(sorted_participants):
                    if sorted_participants[_].Fitness > self.bestParent.Fitness:
                        self._display(sorted_participants[_])
                        self.bestParent = sorted_participants[_]
                        self.historicalFitnesses.append(self.bestParent.Fitness)
                    self.parents.append(sorted_participants[_])
            self.first_run = False

        self.pIndex = self.pIndex - 1 if self.pIndex > 0 else self.lastParentIndex
        self.parent = self.parents[self.pIndex]
        child = sorted_participants[0]
        if self.parent.Fitness > child.Fitness:
            if self.maxAge is None:
                return
            self.parent.Age += 1
            if self.maxAge > self.parent.Age:
                return
            index = bisect_left(self.historicalFitnesses, child.Fitness, 0,
                                len(self.historicalFitnesses))
            difference = len(self.historicalFitnesses) - index
            proportionSimilar = difference / len(self.historicalFitnesses)
            if random.random() < math.exp(-proportionSimilar):
                self.parents[self.pIndex] = child
                return
            self.bestParent.Age = 0
            self.parents[self.pIndex] = self.bestParent
            return
        if not child.Fitness > self.parent.Fitness:
            child.Age = self.parent.Age + 1
            self.parents[self.pIndex] = child
            self._display(child)
            return
        child.Age = 0
        self.parents[self.pIndex] = child
        if child.Fitness > self.bestParent.Fitness:
            self.bestParent = child
            self.historicalFitnesses.append(self.bestParent.Fitness)
            self._display(child)

    def load(self):
        if not os.path.isdir("ai/models/"):
            print("GENETIC: ai/models/ directory not found. Resorting to self-create.")
            length = (INPUT * HIDDEN) + (HIDDEN) + (HIDDEN * OUTPUT) + OUTPUT
            genes = []
            for i in range(length):
                genes.append(self.Geneset[random.randrange(0, len(self.Geneset))])
            return self.lineartonumpy(genes)
        self.loaded_model = True
        # Define initializers, used later for training predictions
        # initialize to float32 for tensorflows used tensor datatype to be compatible
        X_data = tf.placeholder(tf.float32, shape=[None, INPUT], name='x-inputdata')
        y_target = tf.placeholder(tf.float32, shape=[None, OUTPUT], name='y-targetdata')

        # Randomly distribute within the shape input_layer,hidden_layer --> -1 to 1
        # https://www.tensorflow.org/api_docs/python/tf/random_uniform
        weight_one = tf.Variable(tf.random_uniform([INPUT, HIDDEN], -1, 1), name="Weight_One")
        weight_two = tf.Variable(tf.random_uniform([HIDDEN, OUTPUT], -1, 1), name="Weight_Two")

        bias_one = tf.Variable(tf.zeros([HIDDEN]), name="Bias_One")
        bias_two = tf.Variable(tf.zeros([OUTPUT]), name="Bias_Two")

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

        # Save output of training
        saver = tf.train.Saver()

        with tf.Session() as sess:
            saver.restore(sess, "./ai/models/pretrained_car.ckpt")

            # weight_one, bias_one, weight_two, bias_two
            return sess.run(weight_one), sess.run(bias_one), sess.run(weight_two), sess.run(bias_two)

    # x - tuple of numpy arrays
    # Returns linear numpy list
    def numpytolinear(self, x):
        master = x[0].flatten()
        for ary in x[1:]:
            master = np.append(master, ary.flatten())
        return master

    # x - linear numpy array of values
    # Returns tuple of 4 numpy set of w1, b1, w2, b2
    def lineartonumpy(self, x):
        section_w1 = OPTIMIZER + (INPUT * HIDDEN)
        section_b1 = section_w1 + HIDDEN
        section_w2 = section_b1 + (HIDDEN * OUTPUT)
        section_b2 = section_w2 + OUTPUT
        w1 = np.array(x[OPTIMIZER:section_w1])
        b1 = np.array(x[section_w1:section_b1])
        w2 = np.array(x[section_b1:section_w2])
        b2 = np.array(x[section_w2:section_b2])
        w1 = w1.reshape((INPUT, HIDDEN))
        b1 = b1.reshape((HIDDEN,))
        w2 = w2.reshape((HIDDEN, OUTPUT))
        b2 = b2.reshape((OUTPUT,))
        return w1, b1, w2, b2

    class CarSprite(pygame.sprite.Sprite):

        MAX_FORWARD_SPEED = 4
        MAX_REVERSE_SPEED = 2

        def __init__(self, genetic, image, position, chromosome):
            pygame.sprite.Sprite.__init__(self)
            self.src_image = pygame.image.load(image)
            self.position = position
            self.speed = self.direction = self.orientation = 0
            self.k_left = self.k_right = self.k_down = self.k_up = 0
            self.distance = 0
            self.sit_time = 0
            self.history = []
            self.alive = True
            self.win = False
            self.Chromosome = chromosome

            self.Genetic = genetic
            w1, b1, w2, b2 = self.Genetic.lineartonumpy(self.Chromosome.Genes)
            self.Network = network.NeuralNetwork(w1, b1, w2, b2, INPUT, OUTPUT)

        def update(self, deltat):
            # SIMULATION
            self.speed += (self.k_up + self.k_down)
            if self.speed > self.MAX_FORWARD_SPEED:
                self.speed = self.MAX_FORWARD_SPEED
            if self.speed < -self.MAX_REVERSE_SPEED:
                self.speed = -self.MAX_REVERSE_SPEED
            self.direction = (self.direction + (self.k_right + self.k_left)) % 360
            self.orientation = (self.direction + 90) % 360
            x, y = (self.position)
            rad = self.direction * math.pi / 180
            cur_x = x
            cur_y = y
            x += -self.speed * math.sin(rad)
            y += -self.speed * math.cos(rad)
            if cur_x == x and cur_y == y and self.distance == 0:
                self.alive = False
            self.distance += euclidean((cur_x, x), (cur_y, y))
            self.sit_time += 1 if cur_x == x and cur_y == y else 0
            self.position = (x, y)
            self.image = pygame.transform.rotate(self.src_image, self.direction)
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.k_up = self.k_down = self.k_left = self.k_right = 0

        def decision(self, data):
            return self.Network.predict(data)

        def get_car_data(self):
            return [self.position[0], self.position[1], self.speed, self.direction]

        def add_history(self, turn, time=None, distances=None):
            self.history.append(
                History(self.position[0], self.position[1], self.distance, turn, time=time, distances=distances))

    class Chromosome:

        def __init__(self, genes, fitness, strat):
            self.Genes = genes
            self.Fitness = fitness
            self.Strategy = strat
            self.Age = 0

        def __gt__(self, other):
            return self.Fitness > other.Fitness

        def __str__(self):
            return "Genes : {} - Fitness : {}.".format(self.Genes, self.Fitness)


class History:
    def __init__(self, x, y, distance_traveled, turn_choice, time=None, distances=None):
        self.X = x
        self.Y = y
        self.Distance = distance_traveled
        self.Turn = turn_choice
        self.Time = time
        self.Distances = distances

    def get_history(self):
        return self.X, self.Y, self.Distance, self.Turn, self.Time, self.Distances
