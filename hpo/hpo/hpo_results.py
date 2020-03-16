import os
import hpo
import pickle


class Result:
    def __init__(self, model_configuration, score, meta_data=None):
        self._model_configuration = model_configuration
        self._score = score
        self._meta_data = meta_data

    def model_configuration(self):
        return self._model_configuration

    def score(self):
        return self._score

    def meta_data(self):
        return self._meta_data

class Results:
    def __init__(self, meta_data=None, stream_path=None):
        self._stream_path = stream_path
        self._meta_data = meta_data

        self._history = list()

    def add_result(self, result):
        self._history.append(result)

        if self._stream_path is not None:
            self.save(self._stream_path)

    def save(self, path):
        if self._stream_path is not None and os.path.exists(self._stream_path):
            os.remove(self._stream_path)

        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))

        results_file = open(path, "w+b")
        pickle.dump(self, results_file)
        results_file.close()

    @staticmethod
    def load(path):
        results_file = open(path, "rb")
        instance = pickle.load(results_file)
        results_file.close()
        return instance

    def meta_data(self, meta_data=None):
        if meta_data is not None:
            self._meta_data = meta_data

        return self._meta_data

    # returns all model configurations created during the hyper-parameter optimisation stages
    def history(self):
        return self._history

    def best_model(self):
        pass  # TODO