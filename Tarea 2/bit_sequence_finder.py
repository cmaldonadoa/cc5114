from GeneticAlgorithm import GeneticAlgorithm
from Sequence import Sequence
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random

POPULATION_SIZE = 40
MUTATION_RATIO = 0.3


def individual_generator(gene_generator):
    #TARGET = '00101010110101110100011'
    TARGET = '00101010110101'
    return [gene_generator() for _ in range(len(TARGET))]


def gene_generator():
    VOCABULARY = '01'
    return random.choice(VOCABULARY)


def fitness_fun(genes):
    #TARGET = '00101010110101110100011'
    TARGET = '00101010110101'
    fitness = 0
    for gene, target_gene in zip(genes, TARGET):
        fitness += int(gene == target_gene)
    return fitness


def terminate(population, generation):
    #TARGET = '00101010110101110100011'
    TARGET = '00101010110101'
    return population[0].fitness == len(TARGET)


ga = GeneticAlgorithm(POPULATION_SIZE, fitness_fun, gene_generator,
                      MUTATION_RATIO, terminate, individual_generator,
                      Sequence)
ga.run()

# %% Plot max, min and avg fitness by generation
bests = [gen.best for gen in ga.generations]
worsts = [gen.worst for gen in ga.generations]
avgs = [gen.average for gen in ga.generations]
x_axis_values = [gen.n for gen in ga.generations]

fig, ax = plt.subplots()
ax.plot(x_axis_values, bests, 'g', label='Best')
ax.plot(x_axis_values, worsts, 'r', label='Worst')
ax.plot(x_axis_values, avgs, 'b', label='Average')
ax.set(xlabel="Number of generation", ylabel="Fitness")
ax.legend()
fig.set_size_inches(10, 8)

# %% Create heatmap matrix

POPULATION_SIZE_ARRAY = [i for i in range(50, 1000, 50)]
MUTATION_RATIO_ARRAY = [i / 10.0 for i in range(0, 100, 10)]

matrix = []
for mr in MUTATION_RATIO_ARRAY:
    row = []
    for ps in POPULATION_SIZE_ARRAY:
        ga = GeneticAlgorithm(ps, fitness_fun, gene_generator,
                              mr, terminate, individual_generator,
                              Sequence)
        ga.run()
        measure = len(ga.generations)
        row.append(measure)
    matrix.append(row)

# %% Plot heatmap

df = pd.DataFrame(matrix)
fig, ax = plt.subplots(figsize=(20, 10))
ax = sns.heatmap(df,
                 xticklabels=POPULATION_SIZE_ARRAY,
                 yticklabels=MUTATION_RATIO_ARRAY,
                 cbar_kws={'label': 'Generations'})
ax.set(xlabel='Population Size', ylabel='Mutation Ratio')
