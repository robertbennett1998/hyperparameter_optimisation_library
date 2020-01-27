class Data:
    def __init__(self):
        self._training_batch_size = 0
        self._validation_batch_size = 0
        self._test_batch_size = 0

    def load(self):
        pass

    def training_data(self):
        pass

    def validation_data(self):
        pass

    def test_data(self):
        pass

    def training_steps(self):
        pass

    def validation_steps(self):
        pass

    def test_steps(self):
        pass

    def training_batch_size(self, training_batch_size=None):
        if not training_batch_size is None:
            self._training_batch_size = training_batch_size

        return self._training_batch_size

    def validation_batch_size(self, validation_batch_size=None):
        if not validation_batch_size is None:
            self._validation_batch_size = validation_batch_size

        return self._validation_batch_size

    def test_batch_size(self, test_batch_size=None):
        if not test_batch_size is None:
            self._test_batch_size = test_batch_size

        return self._test_batch_size