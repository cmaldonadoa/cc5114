from abc import ABC, abstractmethod


class AbstractIndividual(ABC):
    def __init__(self, individual_generator, fitness_fun,
                 gene_generator, genes=None):
        if genes:
            self.genes = genes
        else:
            self.genes = self._individual_generator(
                individual_generator, gene_generator)
        self.gene_generator = gene_generator
        self.fitness_fun = fitness_fun
        self.fitness = self._calculate_fitness(fitness_fun, self.genes)

    @abstractmethod
    def reproduceWith(self, couple, ratio):
        pass

    # Generate genes for this individual
    def _individual_generator(self, individual, gene):
        return individual(gene)

    # Count number of correct genes

    def _calculate_fitness(self, fitness, genes):
        return fitness(genes)
