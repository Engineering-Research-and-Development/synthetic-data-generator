"""This module tests the trained models router of all his methods"""
import json

import requests

localhost = "http://127.0.0.1:8000/trained_models"

# This is the dummy model we will use for testing purposes
model = {
    "trained_model":
        {
            "name": "TestingModel",
            "dataset_name": "A dataset",
            "size": "100b",
            "input_shape": "(19,29,19)",
            "algorithm_name": "T-VAEs"
        },
    "version":
        {
            "version_name": "Testing version",
            "model_image_path": "A dataset"
        },
    "training_info":
        {
            "loss_function": "TestingTrainInfo",
            "train_loss_value": 100,
            "val_loss_value": 100,
            "n_train_samples": 100,
            "n_validation_samples": 100
        },
    "training_data_info":
        [
            {
                "feature_name": "First feature added to model Testing",
                "feature_position": "0",
                "is_categorical": "true",
                "datatype": "string"
            },
            {
                "feature_name": "Second feature added to model Testing",
                "feature_position": 1,
                "is_categorical": "true",
                "datatype": "string"
            }
        ]
}

def test_get_all_trained_models():
    data = requests.get(localhost)
    assert data.status_code == 200
    payload = data.json()
    # Checking that they are not empty
    for model in payload:
        assert model["name"]
        assert model["id"]
        assert model["dataset_name"]
        assert model["input_shape"]
        assert model["algorithm_name"]
        assert model["size"]

def test_get_trained_models_and_versions():
    data = requests.get(localhost + "/versions")
    assert data.status_code == 200
    payload = data.json()
    for model in payload:
        assert model["name"]
        assert model["id"]
        assert model["dataset_name"]
        assert model["input_shape"]
        assert model["algorithm_name"]
        assert model["size"]
        # This time version_ids can not be empty
        assert model["version_ids"]

def test_get_train_model_id(train_models_test_data) -> bool:
    for model in train_models_test_data:
        data = requests.get(localhost + "/" + str(model['id']))
        assert data.status_code == 200
        data = data.json()
        assert data['size'] == model['size']
        assert data['name'] == model['name']
        assert data['algorithm_name'] == data['algorithm_name']
        assert data['dataset_name'] == model['dataset_name']
        assert data['input_shape'] == model['input_shape']
        assert data['id'] == model['id']

    # Now we try an id that does not exist
    data = requests.get(localhost + "/" + str(10000))
    assert data.status_code == 404

def test_get_all_train_model_versions(train_model_versions):
    # First we check that we get that for all the models we get the versions
    for model in train_model_versions:
        request = requests.get(localhost + "/" + str(model["id"]) + "/versions")
        assert request.status_code == 200
        model_and_versions = request.json()
        assert len(model["versions"]) == len(model_and_versions["versions"])
        for test_version,model_version in zip(model["versions"],model_and_versions["versions"]):
            assert test_version["version_info"]["id"] == model_version["version_info"]["id"]
            assert test_version["training_info"]["id"] == model_version["training_info"]["id"]
        assert len(model["feature_schema"]) == len(model_and_versions["feature_schema"])


def test_delete_a_version():
    """
    This function tests if a delete of a train model works
    :return:
    """
    global model
    payload = json.dumps(model)
    response = requests.post(localhost,payload)
    assert response.status_code == 201
    data = response.json()
    model_id = data["id"]
    response = requests.get(localhost + "/" + str(model_id) + "/versions")
    assert response.status_code != 404
    data = response.json()
    to_del = data["versions"][0]
    response = requests.delete(localhost + "/"+str(model_id)+"/versions/?version_id=" + str(to_del["version_info"]["id"]))
    assert response.status_code == 200
    # Now we check that the version has been deleted
    response = requests.get(localhost + "/"+str(model_id)+"/versions")
    assert response.status_code == 404

def test_create_and_delete_trained_model():
    global model
    payload = json.dumps(model)
    response = requests.post(localhost,payload)
    assert response.status_code != 422
    data = response.json()
    response = requests.get(localhost + "/" + str(data["id"]) +"/versions")
    assert response.status_code != 404
    model = response.json()
    version_id = model["versions"][0]["version_info"]["id"]
    training_info_id = model["versions"][0]["training_info"]["id"]
    # Now we try to delete it, and we check that all the versions and training infos are deleted as well
    assert requests.delete(localhost + "/" + str(data["id"])).status_code == 200
    assert requests.get("http://127.0.0.1:8000/versions/" + str(version_id)).status_code == 404
    assert requests.get("http://127.0.0.1:8000/training_info/" + str(training_info_id)).status_code == 404

