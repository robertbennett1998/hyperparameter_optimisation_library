import numpy
import random
from hpo.hpo_results import Result
import hpo
from tqdm import tqdm
import os
import json


class RandomSearch(hpo.Strategy):
    def __init__(self):
        pass

    def pre_execute(self, model_configuration):
        pass

    def exectue(self, data, model_exception_handler=None):
        pass

    def post_execute(self):
        pass