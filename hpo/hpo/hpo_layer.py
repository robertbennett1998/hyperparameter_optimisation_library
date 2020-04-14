class Layer:
    def __init__(self, layer_name, layer_type, parameters=[], hyperparameters=[]):
        self._layer_name = layer_name
        self._layer_type = layer_type
        self._paramaters = parameters
        
        for parameter in self._paramaters:
            parameter.identifier(self._layer_name + "_" + parameter.name())
        
        self._hyperparameters = hyperparameters
        for hyperparameter in self._hyperparameters:
            hyperparameter.identifier(self._layer_name + "_" + hyperparameter.name())

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
            for hyperparameter in self._hyperparameters:
                hyperparameter.identifier(self._layer_name + "_" + hyperparameter.name())

        return self._hyperparameters