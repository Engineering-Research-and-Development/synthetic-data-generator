import pytest

from ai_lib.data_generator.models.ModelInfo import ModelInfo, AllowedData


@pytest.fixture()
def model_info():
    return ModelInfo(
        default_loss_function="Test Loss Function",
        description="This is a test model",
        allowed_data=[
            AllowedData("int64", False),
            AllowedData("float32", False)
        ],
        name="Test",
    )

def test_get_data(model_info):
    info =  model_info.get_model_info()
    assert info is not None
    assert info["default_loss_function"] == "Test Loss Function"
    assert info["description"] == "This is a test model"
    assert info["name"] == "Test"
    assert len(info["allowed_data"]) == 2
    assert info["allowed_data"][0]["data_type"] == "int64"
    assert info["allowed_data"][0]["is_categorical"] == False
    assert info["allowed_data"][1]["data_type"] == "float32"
    assert info["allowed_data"][1]["is_categorical"] == False
