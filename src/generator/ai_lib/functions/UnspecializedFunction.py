import numpy as np
from abc import ABC, abstractmethod

from ai_lib.functions.Parameter import Parameter


class UnspecializedFunction(ABC):
    def __init__(self, parameters: list[dict]):
        self.parameters = [Parameter.from_json(param) for param in parameters]

    @abstractmethod
    def compute(self, data: np.array):
        raise NotImplementedError

    @abstractmethod
    def _check_parameters(self):
        raise NotImplementedError

    @classmethod
    def self_describe(cls):
        raise NotImplementedError
