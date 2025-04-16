import time
import requests

from conftest import middleware

url = middleware + "/trained_models/"


def check_pushed_models():
    time.sleep(60)
    response = requests.get(url)
    json_response = response.json()
    assert len(json_response["models"]) >= 1


def get_trained_models():
    response = requests.get(url)
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
