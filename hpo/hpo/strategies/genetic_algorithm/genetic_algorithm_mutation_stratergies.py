import math
import random
import time

class MutationStrategy:
    def __init__(self, chromosome_type):
        self._chromosome_type = chromosome_type

    def execute(self, chromosome):
        pass

class PercentageMutationStrategy(MutationStrategy):
    def __init__(self, chromosome_type):
        super(PercentageMutationStrategy, self).__init__(MutationStrategy)
        self._probability = 0.2

    def mutation_probability(self, probability=None):
        if not probability is None:
            if probability > 1.0:
                self._probability = 1.0
            elif probability < 0.0:
                self._probability = 0.0
            else:
                self._probability = probability

        return self._probability

    def execute(self, chromosome):
        threshold = (1.0 - self._probability) * 100
        for gene in chromosome.genes():
            if random.randint(0, 100) >= threshold:
                value_index = 0
                values = random.sample(gene.value_range(), len(gene.value_range()))
                gene.value(values[value_index])
                while not chromosome.check_gene_constraints(gene):
                    value_index += 1
                    gene.value(values[value_index])

        return chromosome

def resolve_mutation_strategy(mutation_strategy, chromosome_type):
    if (mutation_strategy == "percentage"):
        return PercentageMutationStrategy(chromosome_type)