from AbstractIndividual import AbstractIndividual
import random


class Sequence(AbstractIndividual):
    def __init__(self, individual_generator, fitness_fun,
                 gene_generator, genes=None):
        super().__init__(individual_generator, fitness_fun,
                         gene_generator, genes)

    def reproduceWith(self, couple, ratio):
        size = len(self.genes)
        child_genes = []

        # Crossover
        idx = random.choice(range(size - 1))
        child_genes[:idx] = self.genes[:idx]
        child_genes[idx:] = couple.genes[idx:]

        # Mutation
        length = int(ratio * len(child_genes))
        for _ in range(length):
            idx = random.choice(range(size - 1))
            child_genes[idx] = self.gene_generator()

        return Sequence(None,
                        self.fitness_fun,
                        self.gene_generator,
                        child_genes)
