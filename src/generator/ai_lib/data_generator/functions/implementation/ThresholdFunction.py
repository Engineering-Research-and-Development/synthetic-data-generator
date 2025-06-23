from ai_lib.data_generator.functions.UnspecializedFunction import UnspecializedFunction
from ai_lib.data_generator.functions.Parameter import Parameter

import numpy as np

class ThresholdFunction(UnspecializedFunction):
    def __init__(self, data: np.array, parameters: list[dict]):
        super().__init__(data, parameters)
        self.lower_threshold = None
        self.upper_threshold = None
        self.lower_strict = None
        self.upper_strict = None
        self.inner = None
        self._check_parameters()


    def _check_parameters(self):
        assert len(self.parameters) > 1
        param_mapping = {param.name: param for param in self.parameters}
        param_names = param_mapping.keys()
        assert ("lower_threshold" in param_names) or ("upper_threshold" in param_names)
        if "lower_threshold" in param_names:
            assert param_mapping["lower_threshold"].parameter_type == "float"
            assert "lower_strict" in param_names
            assert param_mapping["lower_strict"].parameter_type == "bool"
            self.lower_threshold = param_mapping["lower_threshold"].value
            self.lower_strict = param_mapping["lower_strict"].value
        if "upper_threshold" in param_names:
            assert param_mapping["upper_threshold"].parameter_type == "float"
            assert "upper_strict" in param_names
            assert param_mapping["upper_strict"].parameter_type == "bool"
            self.upper_threshold = param_mapping["upper_threshold"].value
            self.upper_strict = param_mapping["upper_strict"].value

        if "lower_threshold" in param_names and "upper_threshold" in param_names:
            assert param_mapping["lower_threshold"].value < param_mapping["upper_threshold"].value
            assert "inner" in param_names
            assert param_mapping["inner"].parameter_type == "bool"
            self.inner = param_mapping["inner"].value


    def compute(self):
        if self.lower_threshold and self.upper_threshold:
            if self.inner:
                return self.data[(self.data >= self.lower_threshold) & (self.data <= self.upper_threshold)]
            else:
                return self.data[(self.data <= self.lower_threshold) & (self.data >= self.upper_threshold)]

        return self.data