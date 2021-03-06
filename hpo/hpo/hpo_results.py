import os
import hpo
import pickle
import matplotlib.pylab as plt


class Result:
    def __init__(self, model_configuration, training_history, score, final_weights, meta_data=None):
        self._model_configuration = model_configuration
        self._score = score
        self._meta_data = meta_data
        self._training_history = training_history
        self._final_weights = final_weights

    def training_history(self):
        return self._training_history

    def model_configuration(self):
        return self._model_configuration

    def final_weights(self):
        return self._final_weights

    def clear_final_weights(self):
        self._final_weights = None

    def score(self):
        return self._score

    def meta_data(self):
        return self._meta_data


class Results:
    def __init__(self, meta_data=None, result_added_hook=None, stream_path=None):
        self._meta_data = meta_data
        self._result_added_hook = result_added_hook
        self._stream_path = stream_path
        self._highest_score = 0

        self._history = list()

    def add_result(self, result):
        if result.score() < self._highest_score:
            result.clear_final_weights()
        else:
            for res in self._history:
                res.clear_final_weights()
            self._highest_score = int(result.score())

        self._history.append(result)

        if self._stream_path is not None:
            self.save(self._stream_path)

        if self._result_added_hook is not None:
            self._result_added_hook(result=result)

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

    def best_result(self):
        best_score = 0
        best_result = None
        for result in self._history:
            if result is None or result.score() is None:
                continue

            if best_score < result.score():
                best_score = result.score()
                best_result = result
        return best_result