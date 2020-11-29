class Chromosome(object):
    def __init__(self, initial_model_configuration, remote_model_type):
        self._remote_model_type = remote_model_type
        self._age = 0
        self._constraints = None
        self._genes = None
        self._fitness = None
        self._fitness_adjustment = None
        self._model_configuration = initial_model_configuration

    def print(self):
        print("chromosome - Age:", self._age, "Fitness:", self._fitness)
        print(self.decode())

    def fitness_adjustment(self):
        return self._fitness_adjustment

    def age(self):
        return self._age

    def check_constraints(self):
        return True

    def check_gene_constraints(self, gene):
        return True

    def genes(self):
        return self._genes

    def model_configuration(self):
        return self._model_configuration

    def execute(self, data_type, model_exception_handler=None):
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
            decoded_chromosome.append(gene.value())
        return decoded_chromosome