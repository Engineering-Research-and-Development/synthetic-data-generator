import importlib
import json
import pkgutil

import requests
from requests.exceptions import RequestException
import os

from yaml import safe_load

from ai_lib.Exceptions import ModelException
from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from ai_lib.Dataset import Dataset
from .utils import MODEL_FOLDER, create_folder_structure

middleware = os.getenv("MIDDLEWARE_URL", "http://sdg-middleware:8001/")

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


def model_to_middleware(model: UnspecializedModel, data: Dataset):
    feature_list = data.parse_data_to_registry()
    training_info = model.training_info.__dict__
    model_image = model.model_filepath
    model_version = model.check_folder_latest_version(MODEL_FOLDER)
    version_info = {"version_name": model_version, "model_image_path": model_image}
    trained_model_misc = {
        "name": model.model_name,
        "size": model.self_describe().get("size", "Not Available"),
        "input_shape": str(model.input_shape),
        "algorithm_name": model.self_describe().get("name", None)
    }

    model_to_save = {
        "trained_model": trained_model_misc,
        "version": version_info,
        "training_info": training_info,
        "feature_schema": feature_list
    }

    headers = {"Content-Type": "application/json"}
    body = json.dumps(model_to_save)
    try:
        response = requests.post(f"{middleware}trained_models/", headers=headers, data=body)
        if response.status_code > 300:
            raise ModelException("Something went wrong in saving the model, rollback to latest version")
    except RequestException:
        raise ModelException("Impossible to reach Model Repository, rollback to latest version")


def server_startup():
    create_folder_structure()

    config_file = pkgutil.get_data("generator", "config.yaml")
    config = safe_load(config_file)

    id_list = []

    print(config)
    list_models = []
    for pkg in config["system_models"]:
        root = pkg["root_lib"]
        for model in pkg["models"]:
            list_models.append(root+model)

    for model in list_models:
        module_name, class_name = model.rsplit('.', 1)
        module = importlib.import_module(module_name)
        Class = getattr(module, class_name)
        try:
            # TODO: refine with correct APIs
            response = save_system_model(Class.self_describe())
            print(response.status_code, response.text)
            id_list.append(response["id"])
        except ModelException as e:
            for mod_id in id_list:
                delete_sys_model_by_id(mod_id)
            #exit(-1)
