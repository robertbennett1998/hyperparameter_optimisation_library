class Parameter:
    def __init__(self, parameter_name, parameter_value, value_range=None, constraints=None):
        self._parameter_name = parameter_name
        self._parameter_value = parameter_value
        self._value_range = value_range
        self._constraints = constraints

    def get_key_val_pair(self):
        return (self._parameter_name, self._parameter_value)

    def name(self):
        return self._parameter_name

    def value(self, value=None):
        if not value is None:
            self._parameter_value = value

        return self._parameter_value

    def value_range(self):
        return self._value_range

    def constraints(self):
        return self._constraints