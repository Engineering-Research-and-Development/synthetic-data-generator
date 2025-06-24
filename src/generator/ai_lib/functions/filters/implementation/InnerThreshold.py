import numpy as np

from ai_lib.functions.FunctionInfo import FunctionInfo
from ai_lib.functions.Parameter import Parameter
from ai_lib.functions.filters.IntervalThreshold import IntervalThreshold


class InnerThreshold(IntervalThreshold):
    def __init__(self, parameters: list[dict]):
        super().__init__(parameters)

    def compute(self, data: np.array):
        if self.lower_strict:
            upper_indexes = np.greater_equal(data, self.lower_bound)
        else:
            upper_indexes = np.greater(data, self.lower_bound)

        if self.upper_strict:
            lower_indexes = np.less_equal(data, self.upper_bound)
        else:
            lower_indexes = np.less(self.upper_bound)

        final_indexes = lower_indexes & upper_indexes
        return data[final_indexes], final_indexes

    @classmethod
    def self_describe(cls):
        return FunctionInfo(
            name=f"{cls.__qualname__}",
            function_reference=f"{cls.__module__}.{cls.__qualname__}",
            parameters=[
                Parameter("lower_bound", 0.0, "float"),
                Parameter("upper_bound", 1.0, "float"),
                Parameter("lower_strict", True, "bool"),
                Parameter("upper_strict", True, "bool"),
            ],
            description="Filters data between a given interval",
        )
