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

def test_get_all() -> bool:
    data = requests.get(localhost)
    return False if len(data.text) == 0 or data.status_code != 200 else True

def test_get_train_model_by_id() -> bool:
    model_id = 1
    data = requests.get(localhost + "/" + str(model_id))
    if data.status_code != 200:
        return False
    data = data.json()
    if data['size'] != '18B' or data['name'] != 'model3' or data['algorithm_name'] != 'Transformers' \
        or data['dataset_name'] != 'A dataset' or data['input_shape'] != '(2x7x8x4)' or data['id'] != 1:
        return False
    # Now we try an id that doesnt exists
    data = requests.get(localhost + "/" + str(10000))
    if data.status_code != 404:
        return False
    return True

def test_train_model_versions():
    """
    This function checks that for all trained models present in the db we can retrieve the versions info
    :return:
    """
    counter = 0
    while True:
        data = requests.get(localhost + "/" + str(counter) + "/versions")
        if data.status_code == 404:
            break
        data = data.json()
        if len(data["versions"]) == 0:
            return False
        counter += 1

    return True

def test_delete_a_version():
    """
    This function deletes a single version from model with id 1 that currently has 3 versions
    :return:
    """
    response = requests.get(localhost + "/1/versions")
    if response.status_code != 200:
        return False
    data = response.json()
    print("The model has: ",len(data["versions"])," versions")
    before_num_versions = len(data["versions"])
    to_del = data["versions"][0]
    print("Deleting this version:\n",to_del)
    response = requests.delete(localhost + "/1/versions/?version_id=" + str(to_del["version_info"]["id"]))
    if response.status_code != 200:
        return False
    # Now we check that the version has been deleted
    response = requests.get(localhost + "/1/versions")
    data = response.json()
    print("The model has now: ", len(data["versions"]), " versions")
    if len(data["versions"]) >= before_num_versions:
        return False

    return True

def test_create_and_delete_trained_model():
    global model
    payload = json.dumps(model)
    response = requests.post(localhost,payload)
    if response.status_code == 422:
        print(response.text)
        return False
    data = response.json()
    response = requests.get(localhost + "/" + str(data["id"]) +"/versions")
    if response.status_code == 404:
        print("Could not find model")
        return False
    model = response.json()
    print("Fetched model:",model)
    version_id = model["versions"][0]["version_info"]["id"]
    training_info_id = model["versions"][0]["training_info"]["id"]
    # Now we try to delete it, and we check that all the versions and training infos are deleted as well
    if requests.delete(localhost + "/" + str(data["id"])).status_code != 200:
        print("Could not delete model with id:",data["id"])
        return False
    print("Checking if model version with id", str(version_id)," has been deleted")
    if requests.get("http://127.0.0.1:8000/versions/" + str(version_id)).status_code != 404:
        print("Model version has not been deleted correctly")
        return False
    print("Checking if training info with id", str(training_info_id), " has been deleted")
    if requests.get("http://127.0.0.1:8000/training_info/" + str(training_info_id)).status_code != 404:
        print("Training info has not been deleted correctly")
        return False
    return True
