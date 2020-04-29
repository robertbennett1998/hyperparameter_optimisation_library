class ModelBase:
    def __init__(self):
        pass

    def print_summary(self):
        pass

    def weights(self, weights=None):
        pass

    def build(self):
        pass

    def train(self, data_type, exception_callback=None, callbacks=None):
        pass

    def evaluate(self, data_type, exception_callback=None):
        pass

    @staticmethod
    def from_result(result):
        pass

    @staticmethod
    def from_model_configuration(model_configuration, weights=None):
        pass
