import pytest
import numpy as np

from ai_lib.functions.filters.implementation.InnerThreshold import InnerThreshold


@pytest.fixture
def correct_instance():
    data = np.linspace(1,100,100)
    params = [
        {
            "name" : "upper_bound",
            "value": 50.0,
            "parameter_type": "float"
        },
        {
            "name": "lower_bound",
            "value": 10.0,
            "parameter_type": "float"
        },
        {
            "name": "upper_strict",
            "value": True,
            "parameter_type": "bool"
        },
        {
            "name": "lower_strict",
            "value": False,
            "parameter_type": "bool"
        },
    ]
    return InnerThreshold(
        data = data,
        parameters = params
    )

def test_check_parameters(correct_instance):
    param_mapping = {param.name: param for param in correct_instance.parameters}
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