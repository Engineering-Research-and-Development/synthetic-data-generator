import json

import requests
from requests.exceptions import RequestException
from yaml import safe_load
import pkgutil
import os

from exceptions.ModelException import ModelException

config_file = pkgutil.get_data("services", "config.yaml")
config = safe_load(config_file)
model_registry = config["model_registry"]

model_registry_url = os.getenv("MODEL_REGISTRY_URL", model_registry["url"])


def get_trained_model_version_by_id(model_id: int, version_id: int) -> dict:
    """
    Get a specific trained model from repository using both the Model and Version IDs
    :param model_id: the unique identifier of the trained model
    :param version_id: the unique identifier of the version
    :return:
    """
    api = model_registry_url + model_registry["apis"][
        "trained_model_version_by_id"
    ].format(str(model_id), str(version_id))
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
    api = model_registry_url + model_registry["apis"]["trained_model_by_id"].format(
        str(model_id)
    )
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
    api = model_registry_url + model_registry["apis"]["system_models"]
    try:
        response = requests.get(api)
    except RequestException:
        return {}

    return response.json()


def save_trained_model(model_to_send: dict):
    """
    Saves a system model, useful when adding a new feature or to initialize the system
    Must be called after "parse_model_to_registry"
    :param model_to_send: a dictionary containing the model ready to be sent
    :return: None
    """
    headers = {"Content-Type": "application/json"}
    body = json.dumps(model_to_send)
    api = model_registry_url + model_registry["apis"]["trained_models"]
    try:
        response = requests.post(api, headers=headers, data=body)
        if response.status_code > 300:
            raise ModelException(
                "Something went wrong in saving the model, rollback to latest version"
            )
    except RequestException:
        raise ModelException(
            "Impossible to reach Model Repository, rollback to latest version"
        )


def save_system_model(model: dict):
    """
    Saves a system model, useful when adding a new feature or to initialize the system
    :param model: a dictionary containing the model
    :return: None
    """
    headers = {"Content-Type": "application/json"}
    body = json.dumps(model)
    api = model_registry_url + model_registry["apis"]["system_models"]
    try:
        response = requests.post(api, headers=headers, data=body)
        if response.status_code > 300:
            raise ModelException("Something went wrong in initializing the the system")
    except RequestException:
        raise ModelException("Impossible to reach Model Repository")

    return response


def delete_sys_model_by_id(model_id: int):
    """
    Saves a system model, useful when adding a new feature or to initialize the system
    :param model: a dictionary containing the model
    :return: None
    """
    headers = {"Content-Type": "application/json"}
    body = json.dumps({"id": model_id})
    api = model_registry_url + model_registry["apis"]["system_models"]
    try:
        response = requests.delete(api, headers=headers, data=body)
        if response.status_code > 300:
            raise ModelException("Something went wrong in initializing the the system")
    except RequestException:
        raise ModelException("Impossible to reach Model Repository")
