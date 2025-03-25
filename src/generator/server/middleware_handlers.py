import json
import os
from loguru import logger
import requests
from requests.exceptions import ConnectionError
from ai_lib.NumericDataset import NumericDataset
from ai_lib.browse_algorithms import browse_algorithms
from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from server.file_utils import (
    create_server_repo_folder_structure,
    list_trained_models,
    retrieve_model_payload,
)
from server.utilities import format_training_info

middleware = os.environ.get("MIDDLEWARE_URL", "http://sdg-middleware:8001/")
generator_algorithms = []


def server_startup():
    logger.info("Server startup")
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
    logger.info("Server startup completed")


def model_to_middleware(
    model: UnspecializedModel, data: NumericDataset, dataset_name: str, save_path: str
) -> str:
    logger.info(f"Pushing {model.model_name} to the middleware")
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
    logger.info(f"{model.model_name} saved to middleware")
    return body


def sync_trained_models():
    """
    Syncs the trained models from the middleware to the local server.

    This is a very basic sync, it will delete all the models on the server that are not present
    in the middleware. Then it will create all the models on the middleware that are not present
    on the server. This is a very naive approach.

    """
    logger.info("Syncing trained models")
    remote_trained_models = requests.get(f"{middleware}trained_models/").json()
    local_trained_models = list_trained_models()  # Image Paths

    for remote_trained_model in remote_trained_models:
        model_id = remote_trained_model["id"]
        model_payload = requests.get(
            f"{middleware}trained_models/{model_id}?include_versions=true"
        ).json()
        for version in model_payload["versions"]:
            if version["image_path"] not in local_trained_models:
                requests.delete(
                    f"{middleware}trained_models/{model_id}/?version_id={version['id']}"
                )
                logger.info(f"Deleted {model_id} from remote server")
            else:
                local_trained_models.remove(version["image_path"])

    for local_trained_model in local_trained_models:
        local_payload_filepath = retrieve_model_payload(local_trained_model)
        with open(local_payload_filepath, "r") as f:
            model_payload = json.load(f)
        model_to_middleware(
            model_payload["trained_model"],
            model_payload["feature_schema"],
            model_payload["training_info"],
            model_payload["version"],
        )
    logger.info("Sync completed")


def sync_available_algorithms():
    response = requests.get(
        f"{middleware}algorithms/?include_allowed_datatypes=true&indexed_by_names=true"
    )

    remote_algorithms = response.json()
    for algorithm in browse_algorithms():
        for datatype in algorithm["allowed_data"]:
            requests.post(url=f"{middleware}datatypes/", json=datatype)
        if remote_algorithms.get(algorithm["algorithm"]["name"]) is None:
            requests.post(f"{middleware}algorithms/", json=algorithm)
            logger.info(f"Saved {algorithm} to remote server")
        else:
            remote_algorithms.pop(algorithm["algorithm"]["name"])

    # Now we delete all the rest of the stuff from the repo
    for key, val in remote_algorithms.items():
        requests.delete(f"{middleware}algorithms/{val['id']}")
        logger.info(f"Removed {val['id']} to remote server")
