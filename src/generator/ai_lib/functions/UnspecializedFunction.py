import numpy as np
from abc import ABC, abstractmethod

from ai_lib.functions.FunctionResult import FunctionResult
from ai_lib.functions.Parameter import Parameter


class UnspecializedFunction(ABC):
    def __init__(self, parameters: list[dict]):
        self.parameters = [Parameter.from_json(param) for param in parameters]

    @abstractmethod
    def _check_parameters(self):
        raise NotImplementedError

    @abstractmethod
    def _compute(self, data: np.array) -> tuple[np.array, np.array]:
        raise NotImplementedError

    @abstractmethod
    def _evaluate(self, data: np.array) -> bool:
        raise NotImplementedError

    @classmethod
    def self_describe(cls):
        raise NotImplementedError

    def get_results(self, data: np.array) -> dict:
        results, indexes = self._compute(data)
        evaluation_results = self._evaluate(data)
        report = FunctionResult(results, indexes, evaluation_results)
        return report.to_dict()