import hpo
import ray
import hpo.hpo_tensorflow_remote_model


class BayesianMethod(hpo.Strategy):
    def __init__(self, model_configuration, number_of_iterations, surrogate_model, remote_model_type=hpo.hpo_tensorflow_remote_model.TensorFlowRemoteModel):
        super().__init__(remote_model_type)
        self._remote_model_type = remote_model_type
        self._model_configuration = model_configuration
        self._number_of_iterations = number_of_iterations
        self._surrogate_model = surrogate_model

    def execute(self,  data_type, results, model_exception_handler=None):
        remote_model = self._remote_model_type.from_model_configuration(self._model_configuration)
        remote_model.print_summary.remote()
        score = ray.get(remote_model.train.remote(data_type, exception_callback=model_exception_handler))["val_accuracy"][-1]
        self._surrogate_model.add_prior(self._model_configuration.hyperparameter_values(), score)

        for iteration in range(self._number_of_iterations):
            next_config = self._surrogate_model.acquire_best_posterior(self._model_configuration)

            remote_model = self._remote_model_type.from_model_configuration(next_config)
            remote_model.print_summary.remote()

            history_id = remote_model.train.remote(data_type, exception_callback=model_exception_handler)

            history = ray.get(history_id)
            score = history["val_accuracy"][-1]

            results.add_result(hpo.Result(next_config, history, score, ray.get(remote_model.weights.remote()), meta_data={"iteration": iteration}))
            self._surrogate_model.add_prior(next_config.hyperparameter_values(), score)

        return results