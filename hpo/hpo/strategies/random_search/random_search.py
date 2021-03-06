import hpo
import ray
import random
import hpo.hpo_tensorflow_remote_model


class RandomSearch(hpo.Strategy):
    def __init__(self, model_configuration, number_of_iterations, remote_model_type=hpo.hpo_tensorflow_remote_model.TensorFlowRemoteModel):
        super().__init__(remote_model_type)
        self._remote_model_type = remote_model_type
        self._model_configuration = model_configuration
        self._number_of_iterations = number_of_iterations

    def execute(self, data_type, results, model_exception_handler=None):
        for iteration in range(self._number_of_iterations):
            for hyperparameter in self._model_configuration.hyperparameters():
                hyperparameter.value(random.sample(hyperparameter.value_range(), 1)[0])

            remote_model = self._remote_model_type.from_model_configuration(self._model_configuration)
            remote_model.print_summary.remote()

            history_id = remote_model.train.remote(data_type, exception_callback=model_exception_handler)

            history = ray.get(history_id)
            score = history["val_accuracy"][-1]

            results.add_result(hpo.Result(self._model_configuration, history, score, ray.get(remote_model.weights.remote()),
                                          meta_data={"iteration": iteration + 1}))

        return results
