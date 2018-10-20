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

INPUT = 10
HIDDEN = 32
OUTPUT = 4


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def euclidean(dx, dy):
    return np.sqrt((dx[1] - dx[0]) ** 2 + (dy[1] - dy[0]) ** 2)

class GeneticAlgorithm:

    def __init__(self, pool_size=10):
        self.pool = pool_size
        self.crossover_pool = 5
        self.first_run = True
        self.parent = self.bestParent = 0
        self.strategy_pool = ["Create", "Mutate", "Crossover"]
        # takes ~13 seconds on testing system. Called once per class creation
        self.Geneset = list(frange(-1, 1, .0001))
        self.Genelength = (INPUT * HIDDEN) + (HIDDEN * OUTPUT)
        self.maxAge = 5

        self.startTime = 0
        self.parents = []
        self.historicalFitnesses = []
        self.lastParentIndex = (self.crossover_pool - 1) if self.crossover_pool < pool_size else (pool_size - 1)
        self.pIndex = 1

    def _display(self, candidate):
        print("{}-Strategy: {}-{}".format(candidate.Genes, candidate.Strategy, (datetime.datetime.now() - self.startTime)))

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
        participant = self.Chromosome([0 for x in range(length)], 0, "Create")
        for i in range(length):
            participant.Genes[i] = geneset[random.randrange(0, len(geneset))]
        return participant

    def construct_cars(self, car_pos):
        if self.first_run:
            for i in range(self.pool):
                yield self.CarSprite("images/car.png", car_pos, self._create(self.Genelength, self.Geneset))
        else:
            for i in range(self.pool):
                strategy = random.choice(self.strategy_pool)
                if strategy is "Create":
                    yield self.CarSprite("images/car.png", car_pos, self._create(self.Genelength, self.Geneset))
                elif strategy is "Mutate":
                    yield self.CarSprite("images/car.png", car_pos, self._mutate(self.parent, self.Geneset))
                elif strategy is "Crossover":
                    yield self.CarSprite("images/car.png", car_pos, self._crossover(
                        self.parents[random.randrange(0, len(self.parents))],
                        self.parents[random.randrange(0, len(self.parents))]))

    # parameters required such as distance, etc. Possibly capture within car?
    def get_fitness(self, participants, data):
        for participant in participants:
            participant.Chromosome.Fitness = participant.distance - \
                                             euclidean((participant.position[0], data[0]),
                                                                              (participant.position[1], data[1])) + \
                                             data[2] + int(data[3])

    def evaluate_performance(self, participants, data):
        self.get_fitness(participants, data)
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
            return
        child.Age = 0
        self.parents[self.pIndex] = child
        if child.Fitness > self.bestParent.Fitness:
            self.bestParent = child
            self.historicalFitnesses.append(self.bestParent.Fitness)

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
            self.Network = network.NeuralNetwork(chromosome.Genes, INPUT, HIDDEN, OUTPUT)

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
            self.distance += euclidean((cur_x, x), (cur_y, y))
            self.position = (x, y)
            self.image = pygame.transform.rotate(self.src_image, self.direction)
            self.rect = self.image.get_rect()
            self.rect.center = self.position

        def decision(self, data):
            return self.Network.predict(data)

        def get_car_data(self):
            return [self.position[0], self.position[1], self.speed, self.direction, self.distance]

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
