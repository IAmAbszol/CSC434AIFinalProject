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
import numpy as np
from bisect import bisect_left

from ai import network

class GeneticAlgorithm:

    def __init__(self, pool_size=10):
        self.pool = pool_size

    def _crossover(self, participant_a, participant_b, geneset):
        print("")

    def _mutate(self, participant, geneset):
        print("")

    def _create(self, geneset):
        for x in range(self.pool):

    def construct_cars(self, car_pos):


    # parameters required such as distance, etc. Possibly capture within car?
    def get_fitness(self):
        print("")


    def run_ga(self, participant_pool, size, position):

        if participant_pool is None:
            # create participant pool using size
            print("")

    class CarSprite(pygame.sprite.Sprite):

        MAX_FORWARD_SPEED = 10
        MAX_REVERSE_SPEED = 10
        ACCELERATION = 2
        TURN_SPEED = 10

        def __init__(self, image, position, chromosome):
            pygame.sprite.Sprite.__init__(self)
            self.src_image = pygame.image.load(image)
            self.position = position
            self.speed = self.direction = 0
            self.k_left = self.k_right = self.k_down = self.k_up = 0
            self.distance = 0
            self.Chromosome = chromosome
            self.Network = network.NeuralNetwork(self.Chomosome.Genes, len(self.get_car_data()) + 2, 4)

        def update(self, deltat):
            # SIMULATION
            self.speed += (self.k_up + self.k_down)
            if self.speed > self.MAX_FORWARD_SPEED:
                self.speed = self.MAX_FORWARD_SPEED
            if self.speed < -self.MAX_REVERSE_SPEED:
                self.speed = -self.MAX_REVERSE_SPEED
            self.direction += (self.k_right + self.k_left)
            x, y = (self.position)
            rad = self.direction * math.pi / 180
            cur_x = x
            cur_y = y
            x += -self.speed * math.sin(rad)
            y += -self.speed * math.cos(rad)
            self.distance += np.sqrt((x - cur_x) ** 2 + (y - cur_y) ** 2)
            self.position = (x, y)
            self.image = pygame.transform.rotate(self.src_image, self.direction)
            self.rect = self.image.get_rect()
            self.rect.center = self.position

        def decision(self, data):
            print("Printing data for decision, exiting. Delete from genetic.py decision function within car class.\n{}".format(data))
            exit(0)
            return self.Network.predict(data)

        def get_car_data(self):
            return [ self.x, self.y, self.speed, self.direction, self.distance ]

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