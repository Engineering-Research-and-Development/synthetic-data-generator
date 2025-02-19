import json
import requests
from requests.exceptions import RequestException
import os

from ai_lib.Exceptions import ModelException


middleware = os.getenv("MIDDLEWARE_URL", "http://sdg-middleware:8001/")

def get_trained_model_version_by_id(model_id: int, version_id: int) -> dict:
    """
    Get a specific trained model from repository using both the Model and Version IDs
    :param model_id: the unique identifier of the trained model
    :param version_id: the unique identifier of the version
    :return: a dictionary containing model version information
    """
    api = f"{middleware}trained_models/{model_id}/version/{version_id}"
    try:
        response = requests.get(api)
    except RequestException:
        return {}

    return response.json()

def get_trained_model_by_id(model_id: int) -> dict:
    """
    Get a trained model from repository using its ID
    :param model_id: the unique identifier of the model
    :return: a dictionary containing model information
    """
    api = f"{middleware}trained_models/{model_id}"
    try:
        response = requests.get(api)
    except RequestException:
        return {}

    return response.json()

def get_all_system_models() -> dict:
    """
    Returns the list of system models
    :return: the list of models
    """
    api = f"{middleware}algorithms/"
    try:
        response = requests.get(api)
    except RequestException:
        return {}

    return response.json()

def save_trained_model(model_to_send: dict):
    """
    Saves a trained model to the repository
    :param model_to_send: a dictionary containing the model ready to be sent
    :return: None
    """
    headers = {"Content-Type": "application/json"}
    body = json.dumps(model_to_send)
    api = f"{middleware}trained_models/"
    try:
        response = requests.post(api, headers=headers, data=body)
        if response.status_code > 300:
            raise ModelException("Something went wrong in saving the model, rollback to latest version")
    except RequestException:
        raise ModelException("Impossible to reach Model Repository, rollback to latest version")

def save_system_model(model: dict):
    """
    Saves a system model to the repository
    :param model: a dictionary containing the model
    :return: None
    """
    headers = {"Content-Type": "application/json"}
    body = json.dumps(model)
    api = f"{middleware}algorithms/"
    try:
        response = requests.post(api, headers=headers, data=body)
        if response.status_code > 300:
            raise ModelException("Something went wrong in initializing the system")
    except RequestException:
        raise ModelException("Impossible to reach Model Repository")

    return response

def delete_sys_model_by_id(model_id: int):
    """
    Deletes a system model from the repository
    :param model_id: the unique identifier of the model
    :return: None
    """
    headers = {"Content-Type": "application/json"}
    body = json.dumps({"id": model_id})
    api = f"{middleware}algorithms/"
    try:
        response = requests.delete(api, headers=headers, data=body)
        if response.status_code > 300:
            raise ModelException("Something went wrong in deleting the model")
    except RequestException:
        raise ModelException("Impossible to reach Model Repository")