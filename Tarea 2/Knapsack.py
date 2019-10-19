from AbstractIndividual import AbstractIndividual
import random


class Knapsack(AbstractIndividual):
    def __init__(self, individual_generator, fitness_fun,
                 gene_generator, genes=None):
        super().__init__(individual_generator, fitness_fun,
                         gene_generator, genes)

    def reproduceWith(self, couple, ratio):
        MAX_WEIGHT = 15
        child_genes = []

        # Crossover
        # Copy the first idx boxes
        size = len(self.genes)
        idx = 0 if size <= 1 else random.choice(range(size - 1))
        child_genes[:idx] = self.genes[:idx]

        weight = 0
        for gene in child_genes:
            weight += gene.weight

        # Add boxes from the other parent only if possible
        size = len(couple.genes)
        idx = 0 if size <= 1 else random.choice(range(size - 1))
        for gene in couple.genes[idx:]:
            if weight + gene.weight <= MAX_WEIGHT:
                weight += gene.weight
                child_genes.append(gene)

        # Mutation only if possible
        size = len(child_genes)
        length = int(ratio * size)
        for _ in range(length):
            idx = 0 if size <= 1 else random.choice(range(size - 1))
            box = self.gene_generator()
            if weight - child_genes[idx].weight + box.weight <= MAX_WEIGHT:
                weight += box.weight - child_genes[idx].weight
                child_genes[idx] = box

        child_genes = sorted(child_genes, key=lambda x: x.value)

        return Knapsack(None,
                        self.fitness_fun,
                        self.gene_generator,
                        child_genes)
