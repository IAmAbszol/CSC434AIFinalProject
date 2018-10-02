import datetime
import random
import numpy as np
from bisect import bisect_left
from math import exp

def

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