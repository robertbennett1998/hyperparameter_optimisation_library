import hpo
import hpo.strategies.genetic_algorithm as genetic_algorithm
import ray

class Chromosome(object):
    def __init__(self, initial_model_configuration):
        self._age = 0
        self._ranges = None
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

    def gene_ranges(self):
        return self._ranges

    def genes(self):
        return self._genes

    def execute(self, data_type):
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

class DefaultChromosome(Chromosome):
    def __init__(self, initial_model_configuration):
        super().__init__(initial_model_configuration)

        self._genes = list()
        for hyperparameter in self._model_configuration.hyperparameters():
            self._genes.append(genetic_algorithm.Gene(hyperparameter.identifier(), hyperparameter.value_range(), hyperparameter.value(), hyperparameter.constraints()))

    def execute(self, data_type):
        for hyperparameter in self._model_configuration.hyperparameters():
            gene_identifier = hyperparameter.identifier()
            gene = next(x for x in self._genes if x.name() == gene_identifier)
            hyperparameter.value(gene.value())

        remote_model = hpo.RemoteModel.remote(self._model_configuration.optimiser(), self._model_configuration.layers().copy(), self._model_configuration.number_of_epochs())
        remote_model.summary.remote()
        history_id = remote_model.train.remote(data_type)
        history = ray.get(history_id)
        if history is None:
            validation_accuracy = 0
        else:
            validation_accuracy = history["val_accuracy"][-1]

        self._fitness = int(validation_accuracy * 1000)

    def decode(self):
        decoded_chromosome = list()
        for gene in self._genes:
            decoded_chromosome.append((gene.name(), gene.value()))

        return decoded_chromosome