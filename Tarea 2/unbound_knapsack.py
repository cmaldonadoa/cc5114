from GeneticAlgorithm import GeneticAlgorithm
from Knapsack import Knapsack
from collections import namedtuple
import random

POPULATION_SIZE = 20
MUTATION_RATIO = 0.3


def individual_generator(gene_generator):
    MAX_WEIGHT = 15
    genes = []
    weight = 0
    while True:
        box = gene_generator()
        if weight + box.weight <= MAX_WEIGHT:
            genes.append(box)
            weight += box.weight
        else:
            break

    return sorted(genes, key=lambda x: x.value)


def gene_generator():
    Box = namedtuple('Box', 'weight value')
    VOCABULARY = [Box(12, 4), Box(2, 2), Box(1, 2), Box(1, 1), Box(4, 10)]
    return random.choice(VOCABULARY)


def fitness_fun(genes):
    fitness = 0
    for gene in genes:
        fitness += gene.value
    return fitness


def terminate(population, generation):
    return generation == 100


GeneticAlgorithm(POPULATION_SIZE, fitness_fun, gene_generator,
                 MUTATION_RATIO, terminate, individual_generator,
                 Knapsack).run()
