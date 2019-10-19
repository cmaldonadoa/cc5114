import random
from collections import namedtuple


class GeneticAlgorithm(object):
    def __init__(self, population_size, fitness_fun, gene_generator,
                 mutation_rate, terminate, individual_generator,
                 individual_class):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.terminate = terminate

        self.fitness_fun = fitness_fun
        self.gene_generator = gene_generator
        self.individual_generator = individual_generator
        self.individual_class = individual_class

        self.generations = []

    def _tournament(self, population, sample_size):
        sample = random.sample(population, sample_size)
        best = sample[0]
        for individual in sample:
            if individual.fitness > best.fitness:
                best = individual
        return best

    def _calculate_average(self, population):
        n = len(population)
        s = 0
        for individual in population:
            s += individual.fitness
        return s / n

    def run(self):
        generation = 1
        found = False
        population = []
        Generation = namedtuple('Generation', 'n best worst average')

        # Create initial population
        for _ in range(self.population_size):
            population.append(self.individual_class(
                self.individual_generator,
                self.fitness_fun,
                self.gene_generator))

        # Sort the population in descending order by fitness
        population = sorted(
            population, key=lambda x: x.fitness, reverse=True)

        while not found:

            # Check if the solution has been found
            if self.terminate(population, generation):
                found = True
                break

            # Otherwise generate new individuals
            best_parents = []
            sample_size = int(0.1 * self.population_size)

            # Tournament selection
            for _ in range(self.population_size):
                best_parents.append(self._tournament(population, sample_size))

            # Crossover
            new_generation = []
            for _ in range(self.population_size):
                parents = random.sample(best_parents, 2)
                parent1 = parents[0]
                parent2 = parents[1]
                child = parent1.reproduceWith(parent2, self.mutation_rate)
                new_generation.append(child)

            population = sorted(
                new_generation, key=lambda x: x.fitness, reverse=True)

            best = population[0]
            worst = population[self.population_size - 1]
            best_fitness = best.fitness
            worst_fitness = worst.fitness
            average_fitness = self._calculate_average(population)

            self.generations.append(Generation(
                generation, best_fitness, worst_fitness, average_fitness))

            if (generation - 1 % 10) == 0:
                print("Generation: {}\tAverage Fitness: {}\tBest Fitness: {}\
                    \tWorst Fitness: {}".format(generation, average_fitness,
                                                best_fitness, worst_fitness))

            generation += 1

        if generation == 1:
            best = population[0]
            worst = population[self.population_size - 1]
            best_fitness = best.fitness
            worst_fitness = worst.fitness
            average_fitness = self._calculate_average(population)

            self.generations = Generation(
                generation, best_fitness, worst_fitness, average_fitness)

            print("Generation: {}\tAverage Fitness: {}\tBest Fitness: {}\
                \tWorst Fitness: {}".format(generation, average_fitness,
                                            best_fitness, worst_fitness))
