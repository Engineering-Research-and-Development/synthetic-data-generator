import numpy as np
from abc import ABC, abstractmethod

from ai_lib.data_generator.functions.Parameter import Parameter


class UnspecializedFunction(ABC):
    def __init__(self, data: np.array, parameters: list[dict]):
        self.data = data
        self.parameters = [Parameter.from_json(param) for param in parameters]

    @abstractmethod
    def compute(self):
        raise NotImplementedError

    @abstractmethod
    def _check_parameters(self):
        raise NotImplementedError

    @classmethod
    def self_describe(cls):
        raise NotImplementedError
