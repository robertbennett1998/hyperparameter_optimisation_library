class Gene:
    def __init__(self, name, value_range, value, constraints):
        self._name = name
        self._value_range = value_range
        self._value = value
        self._constraints = constraints

    def value_range(self):
        return self._value_range

    def name(self):
        return self._name

    def value(self, value=None):
        if value is None:
            return self._value

        self._value = value

    def constraints(self):
        return self._constraints