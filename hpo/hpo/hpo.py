from hpo.hpo_exceptions import *

class Hpo:
    def __init__(self, model_configuration, data_type, optimisation_strategy):
        self._optimisation_strategy = optimisation_strategy
        self._model_configuration = model_configuration
        self._data_type = data_type

    def execute(self):
        if self._optimisation_strategy is None:
            raise InvalidHpoConfiguration("No optimisation stratergy selected.")

        if self._model_configuration is None:
            raise InvalidHpoConfiguration("No model configuration has being provided.")

        if self._data_type is None:
            raise InvalidHpoConfiguration("No data type has being provided.")

        self._optimisation_strategy.pre_execute(self._model_configuration)

        best_model = self._optimisation_strategy.execute(self._data_type)

        self._optimisation_strategy.post_execute()

        return best_model

    def optimisation_stratergy(self, optimisation_stratergy=None):
        if not optimisation_stratergy is None:
            self._optimisation_strategy = optimisation_stratergy

        return self._optimisation_strategy

    def model_configuration(self, model_configuration=None):
        if not model_configuration is None:
            self._model_configuration = model_configuration

        return self._model_configuration

    def data_type(self, data_type=None):
        if not data_type is None:
            self._data_type = data_type

        return self._data_type