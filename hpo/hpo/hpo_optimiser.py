class Optimiser:
    def __init__(self, optimiser_type, parameters=[], hyperparameters=[], optimiser_name="Optimiser"):
        self._optimiser_type = optimiser_type
        self._parameters = parameters
        self._hyperparameters = hyperparameters
        self._optimiser_name = optimiser_name

    def build(self):
        parameters = self.all_parameters()
        return self._optimiser_type(**parameters)

    def optimiser_name(self, optimiser_name=None):
        if not optimiser_name is None:
            self._optimiser_name = optimiser_name

        return self._optimiser_name

    def optimiser_type(self, optimiser_type=None):
        if not optimiser_type is None:
            self._optimiser_type = optimiser_type

        return self._optimiser_type

    def all_parameters(self):
        paramaters = dict()
        keyVals = [param.get_key_val_pair() for param in self._parameters + self._hyperparameters]
        if len(keyVals) > 0:
            paramaters.update(keyVals)

        return paramaters

    def paramaters(self, parameters=None):
        if not parameters is None:
            self._parameters = parameters

        return self._parameters

    def hyperparameters(self, hyperparameters=None):
        if not hyperparameters is None:
            self._hyperparameters = hyperparameters

        return self._hyperparameters