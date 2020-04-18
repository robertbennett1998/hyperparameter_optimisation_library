import sklearn.preprocessing
import numpy as np

class Parameter:
    def __init__(self, parameter_name, parameter_value, value_range=None, constraints=None, encode_string_values=False):
        self._parameter_name = parameter_name
        self._parameter_value = parameter_value
        self._value_range = value_range
        self._constraints = constraints
        self._encode_string_values = encode_string_values

        if self._encode_string_values:
            self._label_encoder = sklearn.preprocessing.LabelEncoder()
            self._value_range = self._label_encoder.fit_transform(value_range).tolist()
            self._parameter_value = self._label_encoder.transform([self._parameter_value])[0]

        self._identifier = parameter_name

    def get_key_val_pair(self):
        return (self._parameter_name, self.decoded_value())

    def identifier(self, identifier=None):
        if not identifier is None:
            self._identifier = identifier

        return self._identifier

    def name(self):
        return self._parameter_name

    def value(self, value=None):
        if not value is None:
            self._parameter_value = value

        return self._parameter_value

    def decoded_value(self):
        if self._encode_string_values:
            return self._label_encoder.inverse_transform([int(self._parameter_value)])[0]

        return self._parameter_value

    def value_range(self):
        return self._value_range

    def constraints(self):
        return self._constraints

    def serialize(self):
        return self.__dict__

    @staticmethod
    def deserialize(data):
        return Parameter(data["_parameter_name"], data["_parameter_value"], data["_value_range"], data["_constraints"], data["_identifier"])