import hpo.hpo_remote_model
import hpo.hpo_model

class Strategy:
    def __init__(self, model_type=hpo.hpo_model.Model, remote_model_type=hpo.hpo_remote_model.RemoteModel):
        self._model_type = model_type
        self._remote_model_type = remote_model_type

    def pre_execute(self, model_configuration):
        pass

    def execute(self, data_type, results, model_exception_handler=None):
        pass

    def post_execute(self):
        pass