class Strategy:
    def __init__(self):
        pass

    def pre_execute(self, model_configuration):
        pass

    def execute(self, data_type, results, model_exception_handler=None):
        pass

    def post_execute(self):
        pass