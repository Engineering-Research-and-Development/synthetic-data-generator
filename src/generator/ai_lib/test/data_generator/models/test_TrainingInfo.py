import pytest
from ai_lib.data_generator.models.TrainingInfo import TrainingInfo


@pytest.fixture
def training_info():
    return TrainingInfo(
        loss_fn="mse",
        train_samples=100,
        train_loss=0.05,
        validation_samples=20,
        validation_loss=0.03,
    )


def test_training_info_to_dict(training_info):
    assert training_info.to_dict() == {
        "loss_fn": "mse",
        "train_samples": 100,
        "train_loss": 0.05,
        "validation_samples": 20,
        "validation_loss": 0.03,
    }


def test_training_info_to_json(training_info):
    assert (
        training_info.to_json()
        == '{"loss_fn": "mse", "train_samples": 100, "train_loss": 0.05, "validation_samples": 20, "validation_loss": 0.03}'
    )
