import ray
import os
import shutil

class ModelConfiguration:
    def __init__(self, layers=None, number_of_epochs=10):
        self._layers = layers
        self._number_of_epochs = number_of_epochs

    def layers(self, layers=None):
        if not layers is None:
            self._layers = layers
        
        return self._layers

    def number_of_epochs(self, num_of_epochs=None):
        if not num_of_epochs is None:
            self._number_of_epochs = num_of_epochs

        return self._number_of_epochs

@ray.remote(num_gpus=1)
class RemoteModel(object):
    def __init__(self, layers, number_of_epochs=10):
        self._layers = layers
        self._number_of_epochs = number_of_epochs
        self._training_history = None

    def training_history(self):
        return self._training_history

    def number_of_epochs(self, num_of_epochs=None):
        if not num_of_epochs is None:
            self._number_of_epochs = num_of_epochs

        return self._number_of_epochs

    def summary(self):
        print("Model Summary:")
        for layer in self._layers:
            print(layer.layer_name(), ":", sep='')
            for name, value in layer.all_parameters().items():
                print("\t\t", name, "=", value)

    def build(self):
        import tensorflow as tf
        model = tf.keras.models.Sequential()

        for layer in self._layers:
            model.add(layer.build())

        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self, data_type):
        data = data_type()
        data.load()
        model = self.build()

        self._training_history = model.fit(data.training_data(), epochs=self._number_of_epochs, steps_per_epoch=data.training_steps(), validation_data=data.validation_data(), validation_steps=data.validation_steps()).history

        return self._training_history

    def save(self, model_path):
        pass

    def load(self, model_path):
        pass