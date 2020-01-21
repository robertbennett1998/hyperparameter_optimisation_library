from hpo.hpo_exceptions import *

class Hpo:
    def __init__(self, optimisation_stratergy=None, model=None):
        self._optimisation_stratergy = optimisation_stratergy
        self._model = model

    def execute(self):
        if self._optimisation_stratergy is None:
            raise InvalidHpoConfiguration("No optimisation stratergy selected.")

        if self._model is None:
            raise InvalidHpoConfiguration("No model has being provided.")

        self._optimisation_stratergy.pre_execute()
        self._optimisation_stratergy.execute()
        self._optimisation_stratergy.post_execute()

    def optimisation_stratergy(self, optimisation_stratergy=None):
        if not optimisation_stratergy is None:
            self._optimisation_stratergy = optimisation_stratergy

        return self._optimisation_stratergy

    def model(self, model=None):
        if not model is None:
            self._model = model

        return self._model