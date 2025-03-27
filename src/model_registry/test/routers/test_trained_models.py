import pytest
import requests
from fastapi import status

BASE_URL = "http://localhost:8001/trained_models"
train_id = None
version_id = None


def test_create_model_and_version():
    global train_id, version_id
    payload = {
        "model": {
            "name": "Test Model",
            "dataset_name": "Test Dataset",
            "size": "100MB",
            "input_shape": "(1,28,28)",
            "algorithm": 2,
        },
        "version": {
            "version_name": "v1.0",
            "image_path": "/path/to/image",
            "loss_function": "mse",
            "train_loss": 0.1,
            "val_loss": 0.2,
            "train_samples": 100,
            "val_samples": 20,
        },
        "datatypes": [
            {
                "type": "The type of a datatype",
                "is_categorical": True,
                "feature_name": "The name of a feature",
                "feature_position": 0,
            }
        ],
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert "trained_model_id" in response.json()
    assert "model_version_id" in response.json()
    train_id = response.json()["trained_model_id"]
    version_id = response.json()["model_version_id"]


def test_get_all_trained_models():
    response = requests.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("models"), list)


def test_get_trained_model_by_id():
    model_id = train_id
    response = requests.get(f"{BASE_URL}/{model_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "model" in response.json()
    assert "version" in response.json()
    assert "datatypes" in response.json()


def test_delete_trained_model():
    model_id = train_id
    response = requests.delete(f"{BASE_URL}/{model_id}")
    assert response.status_code == status.HTTP_200_OK
