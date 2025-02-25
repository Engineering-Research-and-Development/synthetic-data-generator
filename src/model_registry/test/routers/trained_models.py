"""This module tests the trained models router of all his methods"""

import random
import requests
from copy import deepcopy
from ..conftest import server, port


endpoint = "/trained_models"

# This is the dummy model we will use for testing purposes
model = {
    "trained_model": {
        "name": "TestingModel",
        "dataset_name": "A dataset",
        "size": "100b",
        "input_shape": "(19,29,19)",
        "algorithm_id": 2,
    },
    "version": {"version_name": "Testing version", "image_path": "A dataset"},
    "training_info": {
        "loss_function": "TestingTrainInfo",
        "train_loss": 100,
        "val_loss": 100,
        "train_samples": 100,
        "val_samples": 100,
    },
    "feature_schema": [
        {
            "feature_name": "First feature added to model Testing",
            "feature_position": "0",
            "is_categorical": "true",
            "datatype": "DataType_0",
        },
        {
            "feature_name": "Second feature added to model Testing",
            "feature_position": 1,
            "is_categorical": "true",
            "datatype": "DataType_0",
        },
    ],
}


def test_get_all_trained_models():
    data = requests.get(f"{server}:{port}{endpoint}")
    assert data.status_code == 200, print(data.json())
    payload = data.json()
    # Checking that they are not empty
    assert len(payload) > 0
    rand_tr = random.choice(payload)
    assert rand_tr["name"]
    assert rand_tr["id"]
    assert rand_tr["dataset_name"]
    assert rand_tr["input_shape"]
    assert rand_tr["algorithm_id"]
    assert rand_tr["algorithm_name"]
    assert rand_tr["size"]


def test_get_train_model_and_versions_ids():
    data = requests.get(f"{server}:{port}{endpoint}" + "?include_version_ids=True")
    assert data.status_code == 200, print(data.json())
    payload = data.json()
    # Checking that they are not empty
    assert len(payload) > 0
    for elem in payload:
        assert elem["name"]
        assert elem["id"]
        assert elem["dataset_name"]
        assert elem["input_shape"]
        assert elem["algorithm_id"]
        assert elem["algorithm_name"]
        assert elem["size"]
        if elem["version_ids"]:
            assert len(elem["version_ids"]) > 0


def test_get_train_model_and_versions():
    data = requests.get(f"{server}:{port}{endpoint}" + "/1?include_versions=True")
    assert data.status_code == 200, print(data.json())
    payload = data.json()
    # Checking that they are not empty
    assert len(payload) > 0
    assert payload["name"]
    assert payload["id"]
    assert payload["dataset_name"]
    assert payload["input_shape"]
    assert payload["algorithm_id"]
    assert payload["algorithm_name"]
    assert payload["size"]
    assert payload["versions"]
    assert payload["versions"][0].get("training_info") is None, print(payload)
    assert payload["feature_schema"]


def test_get_train_model_versions_training_info():
    data = requests.get(
        f"{server}:{port}{endpoint}"
        + "/1?include_versions=True&include_training_info=True"
    )
    assert data.status_code == 200, print(data.json())
    payload = data.json()
    # Checking that they are not empty
    assert len(payload) > 0
    assert payload["name"]
    assert payload["id"]
    assert payload["dataset_name"]
    assert payload["input_shape"]
    assert payload["algorithm_id"]
    assert payload["algorithm_name"]
    assert payload["size"]
    assert payload["versions"]
    assert payload["versions"][0]["training_info"]
    assert payload["feature_schema"]


def test_get_train_model_id_with_versions_training_info():
    data = requests.get(
        f"{server}:{port}{endpoint}" + "/2?version_id=1&include_training_info=True"
    )
    assert data.status_code == 200, print(data.json())
    payload = data.json()
    # Checking that they are not empty
    assert len(payload) > 0
    assert payload["name"]
    assert payload["id"]
    assert payload["dataset_name"]
    assert payload["input_shape"]
    assert payload["algorithm_id"]
    assert payload["algorithm_name"]
    assert payload["size"]
    assert payload["versions"]
    assert payload["versions"][0]["training_info"]
    assert payload["feature_schema"]


def test_get_train_model_id_with_bad_versions_training_info():
    data = requests.get(
        f"{server}:{port}{endpoint}" + "/1?version_id=100&include_training_info=True"
    )
    assert data.status_code == 200, print(data.json())
    payload = data.json()
    assert len(payload) > 0
    assert payload["name"]
    assert payload["id"]
    assert payload["dataset_name"]
    assert payload["input_shape"]
    assert payload["algorithm_id"]
    assert payload["algorithm_name"]
    assert payload["size"]
    assert len(payload["versions"]) == 0
    assert payload["feature_schema"]


def test_get_train_model_id_with_bad_versions_good_training_info():
    data = requests.get(
        f"{server}:{port}{endpoint}" + "/1?version_id=1000&include_training_info=True"
    )
    assert data.status_code == 200, print(data.json())
    payload = data.json()
    assert len(payload) > 0
    assert payload["name"]
    assert payload["id"]
    assert payload["dataset_name"]
    assert payload["input_shape"]
    assert payload["algorithm_id"]
    assert payload["algorithm_name"]
    assert payload["size"]
    assert len(payload["versions"]) == 0
    assert payload["feature_schema"]


def test_get_train_model_id_with_bad_versions_bad_training_info():
    data = requests.get(
        f"{server}:{port}{endpoint}" + "/1?version_id=1000&include_training_info=False"
    )
    assert data.status_code == 200, print(data.json())
    payload = data.json()
    assert len(payload) > 0
    assert payload["name"]
    assert payload["id"]
    assert payload["dataset_name"]
    assert payload["input_shape"]
    assert payload["algorithm_id"]
    assert payload["algorithm_name"]
    assert payload["size"]
    assert len(payload["versions"]) == 0
    assert payload["feature_schema"]


def test_get_train_model_id():
    payload = "/1"
    data = requests.get(f"{server}:{port}{endpoint}" + payload)
    assert data.status_code == 200
    payload = data.json()
    assert payload["size"]
    assert payload["name"]
    assert payload["algorithm_id"]
    assert payload["dataset_name"]
    assert payload["input_shape"]
    assert payload["id"]
    assert payload["feature_schema"]


def test_get_bad_id():
    # Now we try an id that does not exist
    data = requests.get(f"{server}:{port}{endpoint}" + "/1000")
    assert data.status_code == 404


def test_get_bad_trained_models_and_versions():
    data = requests.get(
        f"{server}:{port}{endpoint}" + "/1000" + "?include_versions=True"
    )
    assert data.status_code == 404


def test_create_trained_model():
    response = requests.post(f"{server}:{port}{endpoint}", json=model)
    assert response.status_code == 201, print(response.content)
    data = response.json()
    created_id = data["id"]
    assert response.status_code == 201
    # Now we check that it has been saved in the repo
    response = requests.get(
        f"{server}:{port}{endpoint}" + "/" + str(created_id) + "?include_versions=True"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == model["trained_model"]["name"]
    assert len(data["feature_schema"]) == len(model["feature_schema"])


def test_bad_algo_id_create_trained_model():
    bad_data = deepcopy(model)
    bad_data["trained_model"]["algorithm_id"] = 100
    response = requests.post(f"{server}:{port}{endpoint}", json=bad_data)
    assert response.status_code == 400, print(response.content)


def test_bad_datatype_create_trained_model():
    bad_data = deepcopy(model)
    bad_data["feature_schema"][0]["datatype"] = "BadDatatype"
    assert requests.post(f"{server}:{port}{endpoint}", json=bad_data).status_code == 400


def test_delete_bad_train_model():
    assert requests.delete(f"{server}:{port}{endpoint}" + "/100").status_code == 404


def test_delete_train_model():
    # First we create yet again another train model
    response = requests.post(f"{server}:{port}{endpoint}", json=model)
    assert response.status_code == 201, print(response.content)
    model_id = response.json()["id"]
    # We do a get so that we obtain the ids of training infos and model versions
    response = requests.get(
        f"{server}:{port}{endpoint}"
        + "/"
        + str(model_id)
        + "?include_versions=True&include_training_info=True"
    )
    assert response.status_code == 200
    # Now we delete the model and check if it has deleted both the versions and training infos
    assert (
        requests.delete(f"{server}:{port}{endpoint}" + "/" + str(model_id)).status_code
        == 200
    )
    assert (
        requests.get(f"{server}:{port}{endpoint}" + "/" + str(model_id)).status_code
        == 404
    )


def test_delete_train_model_version():
    response = requests.post(f"{server}:{port}{endpoint}", json=model)
    assert response.status_code == 201, print(response.content)
    data = response.json()
    model_id = data["id"]
    # We do a get so that we obtain the ids of training infos and model versions
    response = requests.get(
        f"{server}:{port}{endpoint}"
        + "/"
        + str(model_id)
        + "?include_versions=True&include_training_info=True"
    )
    assert response.status_code == 200
    data = response.json()
    version_id = data["versions"][0]["version"]["id"]
    assert (
        requests.delete(
            f"{server}:{port}{endpoint}"
            + "/"
            + str(model_id)
            + "?version_id="
            + str(version_id)
        ).status_code
        == 200
    )
