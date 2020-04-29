from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import warnings
import scipy
import numpy as np
import random

class SurrogateModel:
    def __init__(self):
        pass

    def add_prior(self, sample, score):
        pass

    def acquire_best_posterior(self, model_configuration):
        pass
    
    def priors(self):
        pass

class GaussianProcessSurrogate(SurrogateModel):
    def __init__(self, kernel=None, sample_size=1000):
        super().__init__()
        self._gpr = GaussianProcessRegressor(kernel=kernel)
        self._sample_size = sample_size

        self._priors_x = None
        self._priors_y = None

    def priors(self):
        return self._priors_x, self._priors_y

    def add_prior(self, sample, score):
        if self._priors_x is None and self._priors_y is None:
            self._priors_x = np.array([sample])
            self._priors_y = np.array([score])
        else:
            self._priors_x = np.vstack((self._priors_x, sample))
            self._priors_y = np.vstack((self._priors_y, score))

        self._gpr.fit(self._priors_x, self._priors_y)

    def acquire_best_posterior(self, model_configuration):
        samples = self._generate_random_samples(model_configuration)

        sample_means, sample_standard_deviations = self._predict_samples_performance(samples)

        if len(sample_means.shape) > 1:
            sample_means = sample_means[:, 0]

        best_prior_mean = self._get_best_prior_mean()
        cdf = scipy.stats.norm.cdf((sample_means - best_prior_mean) / (sample_standard_deviations + 1E-9))
        best_idx = np.argmax(cdf)

        return self._set_hyperparameters(model_configuration, samples[best_idx])

    def _predict_samples_performance(self, samples):
        return self._predict(samples)

    def _get_best_prior_mean(self):
        prior_means, _ = self._predict(self._priors_x)
        return max(prior_means)

    def _predict(self, samples):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return self._gpr.predict(samples, return_std=True)

    def _generate_random_samples(self, model_configuration):
        samples = list()
        for i in range(self._sample_size):
            sample = list()
            for hyperparemeter in model_configuration.hyperparameters():
                sample.append(random.sample(hyperparemeter.value_range(), 1)[0])
            samples.append(np.array(sample))
        return samples

    def _set_hyperparameters(self, model_configuration, config):
        for hyperparemeter, value in zip(model_configuration.hyperparameters(), config):
            hyperparemeter.value(value)

        return model_configuration

class RandomForestSurrogate(SurrogateModel):
    def __init__(self, sample_size=1000):
        super().__init__()
        self._rfr = RandomForestRegressor()
        self._sample_size = sample_size

        self._priors_x = None
        self._priors_y = None

    def priors(self):
        return self._priors_x, self._priors_y

    def add_prior(self, sample, score):
        if self._priors_x is None and self._priors_y is None:
            self._priors_x = np.array([sample])
            self._priors_y = np.array([score])
        else:
            self._priors_x = np.vstack((self._priors_x, sample))
            self._priors_y = np.vstack((self._priors_y, score))

        self._rfr.fit(self._priors_x, self._priors_y)

    def acquire_best_posterior(self, model_configuration):
        samples = self._generate_random_samples(model_configuration)
        print("\n\nSAMPLES:", samples, "\n\n")
        sample_means = self._predict_samples_performance(samples)

        if len(sample_means.shape) > 1:
            sample_means = sample_means[:, 0]

        #best_prior_mean = self._get_best_prior_mean()
        #cdf = scipy.stats.norm.cdf((sample_means - best_prior_mean) / (sample_standard_deviations + 1E-9))
        best_idx = np.argmax(sample_means)

        return self._set_hyperparameters(model_configuration, samples[best_idx])

    def _predict_samples_performance(self, samples):
        return self._predict(samples)

    def _get_best_prior_mean(self):
        prior_means, _ = self._predict(self._priors_x)
        return max(prior_means)

    def _predict(self, samples):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            return self._rfr.predict(samples)

    def _generate_random_samples(self, model_configuration):
        samples = list()
        for i in range(self._sample_size):
            sample = list()
            for hyperparemeter in model_configuration.hyperparameters():
                sample.append(random.sample(hyperparemeter.value_range(), 1)[0])
            samples.append(sample)
        return samples

    def _set_hyperparameters(self, model_configuration, config):
        for hyperparemeter, value in zip(model_configuration.hyperparameters(), config):
            hyperparemeter.value(value)

        return model_configuration


def resolve_surrogate(model, initial_model_configuration):
    if model == "random_forest":
        return RandomForestSurrogate(initial_model_configuration)
    elif model == "gaussian_process":
        return GaussianProcessSurrogate(initial_model_configuration)

    return None