class Layer:
    def __init__(self, layer_name, layer_type, parameters=[], hyperparameters=[]):
        self._layer_name = layer_name
        self._layer_type = layer_type
        self._paramaters = parameters
        self._hyperparameters = hyperparameters

    def build(self):
        parameters = self.all_parameters()
        return self._layer_type(**parameters)

    def layer_name(self, layer_name=None):
        if not layer_name is None:
            self._layer_name = layer_name

        return self._layer_name

    def layer_type(self, layer_type=None):
        if not layer_type is None:
            self._layer_type = layer_type

        return self._layer_type

    def all_parameters(self):
        paramaters = dict()
        keyVals = [param.get_key_val_pair() for param in self._paramaters + self._hyperparameters]
        if len(keyVals) > 0:
            paramaters.update(keyVals)

        return paramaters

    def paramaters(self, paramaters=None):
        if not paramaters is None:
            self._paramaters = paramaters

        return self._paramaters

    def hyperparameters(self, hyperparameters=None):
        if not hyperparameters is None:
            self._hyperparameters = hyperparameters

        return self._hyperparameters