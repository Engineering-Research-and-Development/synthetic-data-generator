import json
import os
from pathlib import Path
from shutil import rmtree
from loguru import logger
import requests
from requests.exceptions import ConnectionError
from ai_lib.NumericDataset import NumericDataset
from ai_lib.browse_algorithms import browse_algorithms
from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from server.file_utils import (
    get_all_subfolders_ids,
    TRAINED_MODELS,
    create_server_repo_folder_structure,
)
from server.utilities import format_training_info

middleware = os.environ.get("MIDDLEWARE_URL", "http://sdg-middleware:8001/")
generator_algorithms = []


def server_startup():
    create_server_repo_folder_structure()
    [generator_algorithms.append(algorithm) for algorithm in browse_algorithms()]
    try:
        sync_trained_models()
        sync_available_algorithms()
    except ConnectionError as error:
        logger.error(
            f"Unable to connect to the middleware. Running in isolated environment\n {error.strerror}"
        )
        return


def model_to_middleware(
    model: UnspecializedModel, data: NumericDataset, dataset_name: str, save_path: str
) -> str | None:
    feature_list = data.parse_data_to_registry()
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
    while response.status_code == 404:
        to_add = response.json()["datatype"]
        datatype_response = requests.post(url=f"{middleware}datatypes/", json=to_add)
        if datatype_response != 201:
            logger.error(
                "Error in creating the datatype",
                to_add,
                " during model save for" " model",
                model_to_save,
            )
            return None
        response = requests.post(
            f"{middleware}trained_models/", headers=headers, data=body
        )

    if response.status_code != 201:
        logger.error(
            f"Something went wrong in saving the model, rollback to latest version\n {response.content}"
        )
        return None
    return str(response.json()["id"])


def sync_trained_models():
    response = requests.get(f"{middleware}trained_models/image-paths/")

    remote_data = response.json()
    for path, trained_id in get_all_subfolders_ids(TRAINED_MODELS):
        # Into posix so that we search it
        if remote_data.get(Path(path).as_posix()) is None:
            rmtree(path)


def sync_available_algorithms():
    response = requests.get(
        f"{middleware}algorithms/?include_allowed_datatypes=true&indexed_by_names=true"
    )

    remote_algorithms = response.json()
    for algorithm in generator_algorithms:
        if remote_algorithms.get(algorithm["algorithm"]["name"]) is None:
            response = requests.post(f"{middleware}algorithms/", json=algorithm)
            # This is the case a datatype is not present
            while response.status_code == 404:
                to_add = response.json()["datatype"]
                datatype_response = requests.post(
                    url=f"{middleware}datatypes/", json=to_add
                )
                if datatype_response != 201:
                    logger.error(
                        "Error in creating the datatype",
                        to_add,
                        " during algorithms sync for" " algorithm",
                        algorithm,
                    )
                    return
                response = requests.post(f"{middleware}algorithms/", json=algorithm)

        else:
            remote_algorithms.pop(algorithm["algorithm"]["name"])

    # Now we delete all the rest of the stuff from the repo
    for key, val in remote_algorithms.items():
        requests.delete(f"{middleware}algorithms/{val['id']}")
