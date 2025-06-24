from ai_lib.functions.UnspecializedFunction import UnspecializedFunction

import numpy as np


class MonoThreshold(UnspecializedFunction):
    def __init__(self, data: np.array, parameters: list[dict]):
        super().__init__(data, parameters)
        self.value = None
        self.strict = None
        self._check_parameters()

    def _check_parameters(self):
        param_mapping = {param.name: param for param in self.parameters}
        self.value = param_mapping["value"].value
        self.strict = param_mapping["strict"].value

    def compute(self):
        raise NotImplementedError

    @classmethod
    def self_describe(cls):
        raise NotImplementedError
