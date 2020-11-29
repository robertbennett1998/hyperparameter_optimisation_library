import hpo.hpo_tensorflow_model


class Strategy:
    def __init__(self, remote_model_type=hpo.hpo_tensorflow_remote_model.TensorFlowRemoteModel):
        self._remote_model_type = remote_model_type

    def pre_execute(self, model_configuration):
        pass

    def execute(self, data_type, results, model_exception_handler=None):
        pass

    def post_execute(self):
        pass