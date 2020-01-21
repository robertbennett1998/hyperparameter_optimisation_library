class Chromosome(object):
    def __init__(self):
        self._age = 0
        self._ranges = None
        self._constraints = None
        self._genes = None
        self._fitness = None
        self._fitness_adjustment = None

    def print(self):
        print("chromosome - Age:", self._age, "Fitness:", self._fitness)
        print(self.decode())

    def fitness_adjustment(self):
        return self._fitness_adjustment

    def age(self):
        return self._age

    def check_constraints(self):
        return True

    def gene_ranges(self):
        return self._ranges

    def genes(self):
        return self._genes

    def execute(self):
        pass

    def fitness(self):
        if not self._fitness_adjustment:
            return self._fitness
        else:
            return self._fitness_adjustment - self._fitness

    def encode(self, values):
        pass

    def decode(self):
        decoded_chromosome = list()
        for gene in self._genes:
            decoded_chromosome.append(gene.value)
        return decoded_chromosome