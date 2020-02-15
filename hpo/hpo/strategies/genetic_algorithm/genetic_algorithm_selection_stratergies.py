from math import ceil
import random
import time

class SurvivorSelectionStratergy:
    def __init__(self):
        pass

    def execute(self, population):
        pass

class FitnessThresholdSelectionStratergy(SurvivorSelectionStratergy):
    def __init__(self, threshold = 0.9):
        super(FitnessThresholdSelectionStratergy, self).__init__()
        self._threshold = threshold

    def _get_upper_lower_chromosone(self, population):
        upperChromosone = population[0]
        lowerChromosone = population[0]
        for chromosone in population:
            if (chromosone.fitness() > upperChromosone.fitness()):
                upperChromosone = chromosone

            if (chromosone.fitness() < lowerChromosone.fitness()):
                lowerChromosone = chromosone

        return upperChromosone, lowerChromosone

    def threshold(self, threshold):
        if not threshold is None:
            if threshold > 1.0:
                self._threshold = 1.0
            elif threshold < 0.0:
                self._threshold = 0.0
            else:
                self._threshold = threshold

        return self._threshold

    def execute(self, population):
        upper, lower = self._get_upper_lower_chromosone(population)
        upperLowerDifference = upper.fitness() - lower.fitness()
        fitnessThreshold = lower.fitness() + (upperLowerDifference * self._threshold)
        for chromosone in population:
            if chromosone.fitness() < ceil(fitnessThreshold):
                population.remove(chromosone)

        return population
    
class RouletteSelectionStrategy(SurvivorSelectionStratergy):
    def __init__(self, survivour_percentage = 0.5):
        super(RouletteSelectionStrategy, self).__init__()
        self._survivour_percentage = survivour_percentage
        print("Roulette Stratergy.")

    def survivour_percentage(self, percentage=None):
        if not percentage is None:
            self._survivour_percentage = percentage

        return self._survivour_percentage

    def execute(self, population):
        total_fitness = 0
        for chromosome in population:
            total_fitness += chromosome.fitness()

        random.seed(time.time())
        for i in range(int(self._survivour_percentage * len(population))):
            value = int(random.uniform(0, total_fitness))
            prev_culmative_value = 0
            culmative_value = 0
            survivours = list()
            for chromosome in population:
                culmative_value += chromosome.fitness()
                if chromosome.fitness() >= prev_culmative_value and chromosome.fitness() < culmative_value:
                    survivours.append(chromosome)

                prev_culmative_value = culmative_value

            return survivours

def resolve_survivour_selection_stratergy(selectionStrat):
    if (selectionStrat == "threshold"):
        return FitnessThresholdSelectionStratergy()
    elif (selectionStrat == "roulette"):
        return RouletteSelectionStrategy()

    return selectionStrat