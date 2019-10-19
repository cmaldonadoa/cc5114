from GeneticAlgorithm import GeneticAlgorithm
from Sequence import Sequence
import random

POPULATION_SIZE = 100
MUTATION_RATIO = 0.3


def individual_generator(gene_generator):
    #TARGET = 'Hello World'
    TARGET = 'helloworld'
    return [gene_generator() for _ in range(len(TARGET))]


def gene_generator():
    #VOCABULARY = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
    VOCABULARY = 'abcdefghijklmnopqrstuvwxyz'
    return random.choice(VOCABULARY)


def fitness_fun(genes):
    #TARGET = 'Hello World'
    TARGET = 'helloworld'
    fitness = 0
    for gene, target_gene in zip(genes, TARGET):
        fitness += int(gene == target_gene)
    return fitness


def terminate(population, generation):
    #TARGET = 'Hello World'
    TARGET = 'helloworld'
    return population[0].fitness == len(TARGET)


GeneticAlgorithm(POPULATION_SIZE, fitness_fun, gene_generator,
                 MUTATION_RATIO, terminate, individual_generator,
                 Sequence).run()
