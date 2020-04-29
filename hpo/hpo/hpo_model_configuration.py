import os
import shutil

class ModelConfiguration:
    def __init__(self, optimiser, layers, loss_function, number_of_epochs):
        self._optimiser = optimiser
        self._layers = layers
        self._loss_function = loss_function
        self._number_of_epochs = number_of_epochs

    def parameters(self):
        p = list()
        p.extend(self._optimiser.paramaters())
        for layer in self._layers:
            p.extend(layer.paramaters())

        return p

    def hyperparameters(self):
        hp = list()
        hp.extend(self._optimiser.hyperparameters())
        for layer in self._layers:
            hp.extend(layer.hyperparameters())

        return hp

    def hyperparameter_values(self):
        hp_values = list()
        hp_values.extend([x.value() for x in self._optimiser.hyperparameters()])
        for layer in self._layers:
            hp_values.extend([x.value() for x in layer.hyperparameters()])

        return hp_values

    def all_parameters(self):
        p = list()
        fp = list()
        fp.extend(self._optimiser.paramaters())
        fp.extend(self._optimiser.hyperparameters())

        for layer in self._layers:
            p.extend(layer.hyperparameters())

        for layer in self._layers:
            p.extend(layer.paramaters())

        p.sort(key=lambda x: x.identifier())
        fp.extend(p)
        return fp

    def layers(self, layers=None):
        if layers is not None:
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

    def number_of_hyperparameter_combinations(self):
        num_of_possible_combinations = 1
        for hp in self.hyperparameters():
            poss_values = len(hp.value_range())
            num_of_possible_combinations *= poss_values
        return num_of_possible_combinations

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

    def optimiser(self, optimiser=None):
        if optimiser is not None:
            self._optimiser = optimiser

        return self._optimiser

    def loss_function(self, loss_function=None):
        if loss_function is not None:
            self._loss_function = loss_function

        return self._loss_function

    def number_of_epochs(self, num_of_epochs=None):
        if num_of_epochs is not None:
            self._number_of_epochs = num_of_epochs

        return self._number_of_epochs