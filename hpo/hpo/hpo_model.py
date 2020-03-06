import ray
import os
import shutil

class ModelConfiguration:
    def __init__(self, optimiser=None, layers=None, number_of_epochs=10):
        self._layers = layers
        self._number_of_epochs = number_of_epochs
        self._optimiser = optimiser

    def hyperparameters(self):
        hyperparamters = list()
        hyperparamters.extend(self._optimiser.hyperparameters())
        for layer in self._layers:
            hyperparamters.extend(layer.hyperparameters())

        return hyperparamters

    def layers(self, layers=None):
        if not layers is None:
            self._layers = layers
        
        return self._layers

    def total_number_of_parameters(self):
        count = 0
        count += len(self._optimiser.all_parameters())
        for layer in self._layers:
            count += len(layer.all_parameters())
        return count

    def number_of_parameters(self):
        count = 0
        count += len(self._optimiser.parameters())
        for layer in self._layers:
            count += len(layer.parameters())
            
        return count

    def number_of_hyperparameters(self):
        count = 0
        count += len(self._optimiser.hyperparameters())
        for layer in self._layers:
            count += len(layer.hyperparameters())

        return count

    def hyperparameter_summary(self, show_values=False):
        num_of_possible_values = 0
        num_of_possible_combinations = 1
        for hp in self.hyperparameters():
            poss_values = len(hp.value_range())
            num_of_possible_combinations *= poss_values
            num_of_possible_values += poss_values
            if show_values:
                print(hp.identifier(), ": ", poss_values, " possible values. Possible values: \n \t", hp.value_range(), sep="")
            else:
                print(hp.identifier(), ": ", poss_values, " possible values.", sep="")
        print(self.number_of_hyperparameters(), "hyperparamters with", num_of_possible_values, "possible values.", num_of_possible_combinations, "(unconstrained) possible combinations.")

    def optimiser(self):
        return self._optimiser

    def number_of_epochs(self, num_of_epochs=None):
        if not num_of_epochs is None:
            self._number_of_epochs = num_of_epochs

        return self._number_of_epochs

@ray.remote
class RemoteModel(object):
    def __init__(self, optimiser, layers, number_of_epochs=10):
        self._optimiser = optimiser
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
        print("", self._optimiser.optimiser_name(), ":", sep='')
        for name, value in self._optimiser.all_parameters().items():
            print("\t\t", name, "=", value)
        for layer in self._layers:
            print(layer.layer_name(), ":", sep='')
            for name, value in layer.all_parameters().items():
                print("\t\t", name, "=", value)

    def build(self):
        import tensorflow as tf
        model = tf.keras.models.Sequential()

        for layer in self._layers:
            model.add(layer.build())

        model.compile(optimizer=self._optimiser.build(), loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def train(self, data_type, callbacks=None):
        import tensorflow as tf
        data = data_type()
        data.load()
        model = self.build()

        earlyStop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=2, verbose=True, mode='min', baseline=None, restore_best_weights=False)
        earlyStop2 = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', min_delta=0, patience=2, verbose=True, mode='max', baseline=None, restore_best_weights=False)
        
        try:
            self._training_history = model.fit(data.training_data(), epochs=self._number_of_epochs, steps_per_epoch=data.training_steps(), validation_data=data.validation_data(), validation_steps=data.validation_steps(), callbacks=[earlyStop, earlyStop2]).history
        except:
            return None
            
        return self._training_history

    def save(self, model_path):
        pass

    def load(self, model_path):
        pass
