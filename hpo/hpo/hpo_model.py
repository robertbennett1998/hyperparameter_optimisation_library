import ray
import os
import shutil
import tensorflow as tf

class Model():
    def __init__(self):
        self._model = None
        self._history = None
        self._layers = None

    def layers(self, layers=None):
        if not layers is None:
            self._layers = layers

        return self._layers

    def build(self):
        pass

    def _train(self, training_dataset, training_steps, validation_dataset=None, validation_steps=0, number_of_epochs=10, cached_model_path=None, history_path=None) -> dict:
        history_logger = None
        if history_path:
            if os.path.exists(history_path):
                os.remove(history_path)

            history_logger = tf.CSVLogger(history_path, append=True, separator=';')

        history = self._model.fit(training_dataset, epochs=number_of_epochs, steps_per_epoch=training_steps, validation_data=validation_dataset, validation_steps=validation_steps)

        if cached_model_path:
            if os.path.exists(cached_model_path):
                shutil.rmtree(cached_model_path)

            print("Saving model (%s)." % cached_model_path)
            self._model.save(cached_model_path)

        self._history = history.history
        print(self._model.summary())
        return history.history

    def history(self) -> dict:
        return self._history