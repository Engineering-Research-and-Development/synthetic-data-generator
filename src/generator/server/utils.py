import importlib
import pkgutil

import os
from yaml import safe_load
from ai_lib.Exceptions import  ModelException
from server.middleware_handlers import save_system_model, delete_sys_model_by_id

ROOT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUTPUT_FOLDER = os.path.join(ROOT_FOLDER, "outputs")
MODEL_FOLDER = os.path.join(OUTPUT_FOLDER, "models")
GENERATION_FOLDER = os.path.join(OUTPUT_FOLDER, "datasets")


def create_folder_structure():
    if not os.path.isdir(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    if not os.path.isdir(MODEL_FOLDER):
        os.mkdir(MODEL_FOLDER)
    if not os.path.isdir(GENERATION_FOLDER):
        os.mkdir(GENERATION_FOLDER)

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