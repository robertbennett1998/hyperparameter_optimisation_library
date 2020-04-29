import hpo
import hpo.strategies.genetic_algorithm as genetic_algorithm
from hpo.strategies.genetic_algorithm.genetic_algorithm_chromosome import Chromosome
import ray


class DefaultChromosome(Chromosome):
    def __init__(self, initial_model_configuration, model_type, remote_model_type):
        super().__init__(initial_model_configuration, model_type, remote_model_type)
        self._remote_model_type = remote_model_type
        self._model_type = model_type

        self._genes = list()
        for hyperparameter in self._model_configuration.hyperparameters():
            self._genes.append(genetic_algorithm.Gene(hyperparameter.identifier(), hyperparameter.value_range(), hyperparameter.value(), hyperparameter.constraints()))

    def execute(self, data_type, model_exception_handler=None):
        for hyperparameter in self._model_configuration.hyperparameters():
            gene_identifier = hyperparameter.identifier()
            gene = next(x for x in self._genes if x.name() == gene_identifier)
            hyperparameter.value(gene.value())

        remote_model = self._remote_model_type.from_model_configuration(self._model_configuration)
        remote_model.print_summary.remote()
        history_id = remote_model.train.remote(data_type, exception_callback=model_exception_handler)
        history = ray.get(history_id)
        if history is None:
            print("WARNING: Exception happened while training model. It was ignored. Imputing 0 as the fitness.")
            validation_accuracy = 0
        else:
            validation_accuracy = history["val_accuracy"][-1]

        self._fitness = int(validation_accuracy * 1000)

        final_weights_id = remote_model.weights.remote()
        return history, ray.get(final_weights_id)

    def decode(self):
        decoded_chromosome = list()
        for gene in self._genes:
            decoded_chromosome.append((gene.name(), gene.value()))

        return decoded_chromosome
