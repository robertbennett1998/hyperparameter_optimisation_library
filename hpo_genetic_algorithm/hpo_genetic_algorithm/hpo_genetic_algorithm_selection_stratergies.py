from math import ceil

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
    
def resolve_survivour_selection_stratergy(selectionStrat):
    if (selectionStrat == "threshold"):
        return FitnessThresholdSelectionStratergy()

    return selectionStrat