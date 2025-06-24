import numpy as np

from ai_lib.functions.FunctionInfo import FunctionInfo
from ai_lib.functions.Parameter import Parameter
from ai_lib.functions.filters.MonoThreshold import MonoThreshold


class LowerThreshold(MonoThreshold):
    def __init__(self, data: np.array, parameters: list[dict]):
        super().__init__(data, parameters)

    def compute(self):
        if self.strict:
            indexes = np.greater_equal(self.data, self.value)
        else:
            indexes = np.greater(self.data, self.value)
        return self.data[indexes], indexes

    @classmethod
    def self_describe(cls):
        return FunctionInfo(
            name=f"{cls.__qualname__}",
            function_reference=f"{cls.__module__}.{cls.__qualname__}",
            parameters=[
                Parameter("value", 0.0, "float"),
                Parameter("strict", True, "bool"),
            ],
            description="Mono-threshold function: pick values greater than a lower threshold",
        )
