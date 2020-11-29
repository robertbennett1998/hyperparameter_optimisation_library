class ModeLConfigurationBase:
    def __init__(self, layers):
        self._layers = layers

    def parameters(self):
        pass

    def parameter_values(self):
        pass

    def hyperparameters(self):
        pass

    def hyperparameter_values(self):
        pass

    def all_parameters(self):
        pass

    def layers(self, layers=None):
        pass

    def print_hyperparameter_summary(self, show_values=False):
        pass