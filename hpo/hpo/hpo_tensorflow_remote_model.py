import ray
import os
import shutil

@ray.remote(num_gpus=1)
class TensorFlowRemoteModel(object):
    def __init__(self, optimiser, layers, loss_function, number_of_epochs, weights=None):
        self._optimiser = optimiser
        self._layers = layers
        self._loss_function = loss_function
        self._number_of_epochs = number_of_epochs
        self._training_history = None
        self._weights = weights

    def print_summary(self):
        print("Model Summary:")
        print("", self._optimiser.optimiser_name(), ":", sep='')
        for name, value in self._optimiser.all_parameters().items():
            print("\t\t", name, "=", value)
        for layer in self._layers:
            print(layer.layer_name(), ":", sep='')
            for name, value in layer.all_parameters().items():
                print("\t\t", name, "=", value)

    def weights(self, weights=None):
        if weights is not None:
            self._weights = weights

        return self._weights

    def build(self):
        import tensorflow as tf
        model = tf.keras.models.Sequential()

        for layer in self._layers:
            model.add(layer.build())

        model.compile(optimizer=self._optimiser.build(), loss=self._loss_function, metrics=['accuracy'])

        return model

    def train(self, data_type, exception_callback=None, callbacks=None):
        data = data_type()
        data.load()
        model = self.build()

        if self._weights is not None:
            model.set_weights(self._weights)

        try:
            self._training_history = model.fit(data.training_data(),
                                               epochs=self._number_of_epochs,
                                               steps_per_epoch=data.training_steps(),
                                               validation_data=data.validation_data(),
                                               validation_steps=data.validation_steps(),
                                               callbacks=callbacks).history
        except Exception as e:
            if exception_callback is not None:
                exception_callback(e)
            else:
                raise
            return None

        self._weights = model.get_weights().copy()
        return self._training_history

    def evaluate(self, data_type, exception_callback=None):
        data = data_type()
        data.load()
        model = self.build()

        if self._weights is not None:
            model.set_weights(self._weights)

        try:
            self._training_history = model.evaluate(data.training_data()).history
        except Exception as e:
            if exception_callback is not None:
                exception_callback(e)
            else:
                raise
            return None

        return self._training_history

    @staticmethod
    def from_result(result):
        return TensorFlowRemoteModel.remote(result.model_configuration.optimiser(), result.model_configuration.layers().copy(), result.model_configuration.loss_function(), result.model_configuration.number_of_epochs(), result.final_weights())

    @staticmethod
    def from_model_configuration(model_configuration, weights=None):
        return TensorFlowRemoteModel.remote(model_configuration.optimiser(), model_configuration.layers().copy(), model_configuration.loss_function(), model_configuration.number_of_epochs(), weights)
