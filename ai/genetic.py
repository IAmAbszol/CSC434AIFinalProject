import pygame
import math
import datetime
import random
import numpy as np
from bisect import bisect_left

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
        self.Chromosome = chromosome

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
        x += -self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)
        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

def _crossover(participant_a, participant_b, geneset):

def _mutate(participant, geneset):

def _create(geneset):

# parameters required such as distance, etc. Possibly capture within car? 
def get_fitness():


def run_ga(participant_pool, size, position):

    if participant_pool is None:
        # create participant pool using size




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