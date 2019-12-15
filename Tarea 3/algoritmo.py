import random
from collections import namedtuple
import numpy as np


class GeneticAlgorithm(object):
    def __init__(self, population_size, fitness_fun, mutation_rate,
                 tree_generator, target, var="", points=[], max_deep=10, limit=10000):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.target = target
        self.fitness_fun = fitness_fun

        self.tree_generator = tree_generator
        self.generations = []

        self.limit = limit
        self.max_deep = max_deep
        self.var = var
        self.points = points

    def _tournament(self, population, sample_size):        

        fitness_args = [self.target]
        if self.var != "":
            fitness_args += [self.var, self.points]
        weights = sorted(np.random.dirichlet(np.ones(len(population)) * 4, size=1)[0], reverse=True)
        sample = np.random.choice(population, sample_size, p=weights)
        bests = sorted(
            sample, key=lambda x: self.fitness_fun(x, *fitness_args))
        return bests[0]

    def run(self):
        generation = 1
        population = []
        Generation = namedtuple('Generation', 'n best worst')

        fitness_args = [self.target]
        if self.var != "":
            fitness_args += [self.var, self.points]

        # Create initial population
        for _ in range(self.population_size):
            population.append(self.tree_generator(self.max_deep))

        # Sort the population in ascending order by fitness
        population = sorted(
            population, key=lambda x: self.fitness_fun(x, *fitness_args))

        # Put negatives at the end (these will be the ones with division by 0)
        i = len(population)
        while i > 0:
            if self.fitness_fun(population[0], *fitness_args) < 0:
                x = population.pop(0)
                population += [x]
            else:
                break
            i -= 1

        while generation <= self.limit:

            # Check if the solution has been found
            # CASE: no variables
            if self.var == "":
                if population[0].eval() == self.target:
                    break
            # CASE: variables
            else:
                exacts = 0
                for point in self.points:
                    d = {self.var: point}
                    if population[0].eval(d) == self.target.eval(d):
                        exacts += 1
                if exacts == len(self.points):
                    break

            # Otherwise generate new individuals
            best_parents = []
            sample_size = int(0.2 * len(population))

            # Tournament selection
            for _ in range(len(population)):
                best_parents.append(self._tournament(population, sample_size))

            # Crossover
            new_generation = []
            for _ in range(self.population_size):
                parents = random.sample(best_parents, 2)
                parent1 = parents[0]
                parent2 = parents[1]
                child = parent1.copy()

                prob = random.random()
                if prob > self.mutation_rate:
                    p2 = parent2.select().copy()
                    child.select_replace(p2)
                    new_generation.append(child)
                else:
                    p2 = self.tree_generator(self.max_deep)
                    child.select_replace(p2)
                    new_generation.append(child)

            population = sorted(
                new_generation, key=lambda x: self.fitness_fun(x, *fitness_args))

            i = len(population)
            while i > 0:
                if self.fitness_fun(population[0], *fitness_args) < 0:
                    x = population.pop(0)
                    population += [x]
                else:
                    break
                i -= 1

            best = population[0]
            worst = population[-1]
            best_fitness = self.fitness_fun(best, *fitness_args)
            worst_fitness = self.fitness_fun(worst, *fitness_args)

            self.generations.append(Generation(
                generation, best_fitness, worst_fitness))

            if ((generation - 1) % 10) == 0:
                print("Generation: {} \tTarget: {} \
                      \nFitness    Best: {}    Worst: {}".format(generation, self.target, best_fitness, worst_fitness))
                print("Best tree: {}".format(best))
            generation += 1


        best = population[0]
        worst = population[-1]
        best_fitness = self.fitness_fun(best, *fitness_args)
        worst_fitness = self.fitness_fun(worst, *fitness_args)

        if (generation == 1):
            self.generations.append(Generation(
                generation, best_fitness, worst_fitness))

        print("======== RESULT ========")
        print("Generation: {} \tTarget: {} \
              \nFitness    Best: {}    Worst: {}".format(generation, self.target, best_fitness, worst_fitness))
        print("Best tree: {}".format(best))
        print("========================")