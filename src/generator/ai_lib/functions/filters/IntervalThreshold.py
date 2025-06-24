from ai_lib.functions.UnspecializedFunction import UnspecializedFunction

import numpy as np


class IntervalThreshold(UnspecializedFunction):
    def __init__(self, data: np.array, parameters: list[dict]):
        super().__init__(data, parameters)
        self.upper_bound = None
        self.lower_bound = None
        self.upper_strict = None
        self.lower_strict = None
        self._check_parameters()

    def _check_parameters(self):
        param_mapping = {param.name: param for param in self.parameters}
        param_names = param_mapping.keys()
        assert param_mapping["upper_bound"].value > param_mapping["lower_bound"].value
        assert isinstance(param_mapping["upper_bound"].value, float)
        assert isinstance(param_mapping["lower_bound"].value, float)
        assert isinstance(param_mapping["upper_strict"].value, bool)
        assert isinstance(param_mapping["lower_strict"].value, bool)
        assert "upper_bound" in param_names
        assert "lower_bound" in param_names
        assert "upper_strict" in param_names
        assert "lower_strict" in param_names
        self.upper_bound = param_mapping["upper_bound"].value
        self.lower_bound = param_mapping["lower_bound"].value
        self.upper_strict = param_mapping["upper_strict"].value
        self.lower_strict = param_mapping["lower_strict"].value

    def compute(self):
        raise NotImplementedError

    @classmethod
    def self_describe(cls):
        raise NotImplementedError
