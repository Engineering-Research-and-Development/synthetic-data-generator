import json
import os
from pathlib import Path
from shutil import rmtree
from loguru import logger
import requests

from ai_lib.NumericDataset import NumericDataset
from ai_lib.browse_algorithms import browse_algorithms
from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from server.file_utils import get_all_subfolders_ids

middleware = os.environ.get("MIDDLEWARE_URL", "http://sdg-middleware:8001/")
generator_algorithms = []


def model_to_middleware(
    model: UnspecializedModel, data: NumericDataset, dataset_name: str, save_path: str
) -> str | None:
    feature_list = data.parse_data_to_registry()
    create_datatypes_if_not_present(feature_list)
    training_info = format_training_info(model.training_info.to_dict())
    model_image = save_path
    model_version = "v0"
    version_info = {
        "version_name": model_version,
        "image_path": model_image,
    }  # Version management as described above
    # Getting the algorithm id
    response = requests.get(
        f"{middleware}algorithms/name/{model.self_describe().get('name', None)}"
    )
    # This edge case should not be happening since the existence of the algorithm is checked before this function
    if response.status_code != 200:
        raise SystemError
    algorithm_id = response.json()["id"]
    trained_model_misc = {
        "name": model.model_name,
        "size": model.self_describe().get("size", "Not Available"),
        "input_shape": str(model.input_shape),
        "algorithm_id": algorithm_id,
        "dataset_name": dataset_name,
    }

    model_to_save = {
        "trained_model": trained_model_misc,
        "version": version_info,
        "training_info": training_info,
        "feature_schema": feature_list,
    }

    headers = {"Content-Type": "application/json"}
    body = json.dumps(model_to_save)
    response = requests.post(f"{middleware}trained_models/", headers=headers, data=body)
    if response.status_code != 201:
        logger.error(
            f"Something went wrong in saving the model, rollback to latest version\n {response.content}"
        )
        return None
    return str(response.json()["id"])


def create_datatypes_if_not_present(feature_list: list[dict]):
    response = requests.get(f"{middleware}datatypes/?index_by_id=true")
    if response.status_code != 200:
        logger.error(
            f"Could not reach model repo for datatypes validation\n"
            f"{response.status_code}:{response.content}"
        )
    remote_dt = response.json()
    for feature in feature_list:
        # This means the datatype is not present, so in order to use this algo we must create it
        if remote_dt.get(feature["datatype"]) is None:
            payload = {
                "datatype": feature["datatype"],
                "is_categorical": feature["is_categorical"],
            }
            requests.post(url=f"{middleware}datatypes/", json=payload)


def format_training_info(tr_info: dict):
    payload = {
        "loss_function": tr_info["loss_fn"],
        "train_loss": tr_info["train_loss"],
        "val_loss": tr_info["validation_loss"],
        "train_samples": tr_info["train_samples"],
        "val_samples": tr_info["validation_samples"],
    }
    return payload


def server_startup(app_folder: str):
    # 1. Sync with any new implemented trained models and Sync with remote
    sync_remote_trained("trained_models/image-paths/", app_folder)
    # 1. Sync with any new implemented algorithms and Sync with remote
    sync_remote_algorithm()


def sync_remote_trained(endpoint: str, folder: str):
    response = requests.get(f"{middleware}{endpoint}")
    remote_data = response.json()
    for path, trained_id in get_all_subfolders_ids(
        os.path.join(folder, Path("saved_models/trained_models"))
    ):
        # Into posix so that we search it
        if remote_data.get(Path(path).as_posix()) is None:
            rmtree(path)


def sync_remote_algorithm():
    global generator_algorithms
    # Since the generator offers a method that lists all the implemented algorithms we only
    # need to do a sync with the remote repository
    response = requests.get(
        f"{middleware}algorithms/?include_allowed_datatypes=true&indexed_by_names=true"
    )
    remote_algorithms = response.json()
    for algorithm in browse_algorithms():
        # Creating a local data structure that we keep in memory
        generator_algorithms.append(algorithm)
        if remote_algorithms.get(algorithm["algorithm"]["name"]) is None:
            check_algorithm_datatypes(algorithm["allowed_data"])
            requests.post(f"{middleware}algorithms/", json=algorithm)
        else:
            remote_algorithms.pop(algorithm["algorithm"]["name"])

    # Now we delete all the rest of the stuff from the repo
    for key, val in remote_algorithms.items():
        requests.delete(f"{middleware}algorithms/{val['id']}")


def check_algorithm_datatypes(datatypes: list[dict[str, str | bool]]):
    response = requests.get(f"{middleware}datatypes/?index_by_id=true")
    remote_dt = response.json()
    for datatype in datatypes:
        # This means the datatype is not present, so in order to use this algo we must create it
        if remote_dt.get(datatype["data_type"]) is None:
            payload = {
                "datatype": datatype["data_type"],
                "is_categorical": datatype["is_categorical"],
            }
            requests.post(url=f"{middleware}datatypes/", json=payload)
