class Parameter:
    def __init__(self, name, value, value_range=None, constraints=None):
        self._name = name
        self._value = value
        self._value_range = value_range
        self._constraints = constraints

    def get_key_val_pair(self):
        return (self._name, self._value)

    def name(self):
        return self._name

    def value(self, value=None):
        if not value is None:
            self._value = value

        return self._value

    def value_range(self):
        return self._value_range

    def constraints(self):
        return self._constraints