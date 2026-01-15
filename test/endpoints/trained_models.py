import time
import requests

from conftest import SERVICE_CONFIG

URL = f"{SERVICE_CONFIG.middleware}/trained_models/"
TRAINING_TIME = 30


def check_pushed_model(model_name: str):
    time.sleep(TRAINING_TIME)
    response = requests.get(URL)
    json_response = response.json()
    assert len(json_response["models"]) >= 1
    assert model_name in [
        model_entry["model"]["name"]
        for model_entry in json_response["models"]
        if model_entry["model"]["name"] == model_name
    ]


def get_trained_models():
    response = requests.get(URL)
    json_response = response.json()
    return json_response


def get_versions_by_trained_model_name(data: dict, trained_model_name: str):
    return [
        version["version_name"]
        for model_entry in data.get("models", [])
        if model_entry.get("model", {}).get("name") == trained_model_name
        for version in model_entry.get("versions", [])
    ]


def get_trained_model_id_by_trained_model_name(data: dict, trained_model_name: str):
    return [
        model_entry.get("model", {}).get("id")
        for model_entry in data.get("models", [])
        if model_entry.get("model", {}).get("name") == trained_model_name
    ]
