import math
import random
import time

class CrossoverStratergy:
    def __init__(self, chromosomeType):
        self._chromosomeType = chromosomeType
        random.seed(time.time())

    def execute(self, chromosomeOne, chromosomeTwo):
        pass

class OnePointCrossover(CrossoverStratergy):
    def __init__(self, chromosomeType):
        super(OnePointCrossover, self).__init__(chromosomeType)

    def execute(self, chromosomeOne, chromosomeTwo):
        newchromosome = self._chromosomeType()

        length = math.ceil(len(newchromosome.genes()) / 2)

        for i in range(length):
            newchromosome.genes()[i].value(chromosomeTwo.genes()[i].value())

        for i in range(length, len(newchromosome.genes())):
            newchromosome.genes()[i].value(chromosomeOne.genes()[i].value())

        for gene in newchromosome.genes():
            while not newchromosome.check_gene_constraints(gene):
                val = random.sample(gene.value_range(), 1)
                gene.value(val[0])

        return newchromosome

class UniformCrossover(CrossoverStratergy):
    def __init__(self, chromosomeType):
        super(UniformCrossover, self).__init__(chromosomeType)

    def execute(self, chromosomeOne, chromosomeTwo):
        newchromosome = self._chromosomeType()
        length = len(newchromosome.genes())

        for i in range(length):
            if (random.randint(0, 100) > 50):
                setattr(newchromosome, newchromosome.genes()[i], getattr(chromosomeOne, chromosomeOne.genes()[i]))
            else:
                setattr(newchromosome, newchromosome.genes()[i], getattr(chromosomeTwo, chromosomeTwo.genes()[i]))

        for chromosome in (chromosomeOne, chromosomeTwo):
            for gene in chromosome.genes():
                while not chromosome.check_gene_constraints(gene):
                    val = random.sample(chromosome._ranges[gene], 1)
                    setattr(chromosome, gene, val[0])

        return newchromosome

class NPointCrossover(CrossoverStratergy):
    def __init__(self, chromosomeType):
        super(NPointCrossover, self).__init__(chromosomeType)

        self._segmentLength = 1

    def execute(self, chromosomeOne, chromosomeTwo):
        newchromosome = self._chromosomeType()
        length = len(newchromosome.genes())
        currentchromosome = chromosomeOne

        for i in range(length):
            setattr(newchromosome, newchromosome.genes()[i], getattr(currentchromosome, currentchromosome.genes()[i]))

            if (i % self._segmentLength == 0):
                if currentchromosome == chromosomeOne:
                    currentchromosome = chromosomeTwo
                else:
                    currentchromosome = chromosomeOne

        for chromosome in (chromosomeOne, chromosomeTwo):
            for gene in chromosome.genes():
                value_index = 0
                values = random.sample(gene.value_range(), len(gene.value_range()))
                while not chromosome.check_gene_constraints(gene):
                    gene.value(values[value_index])
                    value_index += 1

        return newchromosome

    def segment_length(self, segmentLength=None):
        chromosome = self._chromosomeType()
        if not segmentLength is None:
            if segmentLength < 1:
                self._segmentLength = 1
            elif segmentLength > len(chromosome.genes()) - 1:
                self._segmentLength = len(chromosome.genes()) - 1
            else:
                self._segmentLength = segmentLength

        return self._segmentLength 

def resolve_crossover_stratergy(xStrat, chromosomeType):
    if (xStrat == "onepoint"):
        return OnePointCrossover(chromosomeType)
    elif (xStrat == "uniform"):
        return UniformCrossover(chromosomeType)
    elif (xStrat == "npoint"):
        return NPointCrossover(chromosomeType)
    return xStrat