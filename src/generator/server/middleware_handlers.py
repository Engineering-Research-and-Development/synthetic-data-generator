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
    delete_folder,
    get_folder_full_path, save_model_payload,
)

MIDDLEWARE_ON = True
middleware = os.environ.get("MIDDLEWARE_URL", "http://sdg-middleware:8001/")
GENERATOR_ALGORITHM_NAMES = []
ALGORITHM_LONG_NAME_TO_ID = {}
ALGORITHM_LONG_TO_SHORT = {}
ALGORITHM_SHORT_TO_LONG = {}


def server_startup():
    """
    Called at server startup to initialize the server.
    It creates a folder structure for saving models on the server and
    syncs the available algorithms from the middleware to the local server.
    """
    logger.info("Server startup")
    create_server_repo_folder_structure()
    [
        GENERATOR_ALGORITHM_NAMES.append(algorithm["algorithm"]["name"])
        for algorithm in browse_algorithms()
    ]
    for algorithm in GENERATOR_ALGORITHM_NAMES:
        ALGORITHM_LONG_TO_SHORT[algorithm] = algorithm.split(".")[-1]
        ALGORITHM_SHORT_TO_LONG[ALGORITHM_LONG_TO_SHORT[algorithm]] = algorithm

    try:
        sync_available_algorithms()
        sync_trained_models()
    except ConnectionError as error:
        global MIDDLEWARE_ON
        MIDDLEWARE_ON = False
        logger.error(
            f"Unable to connect to the middleware. Running in isolated environment\n {error.strerror}"
        )
        return
    logger.info("Server startup completed")


def model_to_middleware(
    model: UnspecializedModel,
    data: NumericDataset,
    dataset_name: str,
    save_path: str,
    version_name: str,
) -> str:
    """
    Pushes a trained model to the middleware.

    This function logs the process of pushing a trained model to the middleware.
    It gathers necessary information from the model and dataset, such as feature list
    and training information, and constructs a payload to send to the middleware.
    The payload includes model metadata, version information, and datatype details.
    The function ultimately posts the model to the middleware for storage and returns
    the response body of the POST request.

    :param model: The trained model to be pushed
    :param data: The dataset used for training the model
    :param dataset_name: The name of the dataset
    :param save_path: The path where the model is saved
    :param version_name: The version name of the model
    :return: The response body of the POST request
    """

    feature_list = data.parse_data_to_registry()
    training_info = model.training_info.to_dict()
    version_info = {
        "version_name": version_name,
        "image_path": save_path,
    }
    # Getting the algorithm id
    algorithm_id = ALGORITHM_LONG_NAME_TO_ID.get(
        model.self_describe().get("algorithm").get("name")
    )
    trained_model_misc = {
        "name": model.model_name,
        "dataset_name": dataset_name,
        "size": model.self_describe().get("size", "Not Available"),
        "input_shape": str(model.input_shape).replace(" ", ""),
        "algorithm": algorithm_id,
        "algorithm_long_name": model.self_describe().get("algorithm").get("name"),
    }
    version_info.update(training_info)
    model_to_save = {
        "model": trained_model_misc,
        "version": version_info,
        "datatypes": feature_list,
    }
    return post_model_to_middleware(model_to_save)


def post_model_to_middleware(model_to_save: dict):
    """
    Posts a trained model to the middleware

    :param model_to_save: The model to be saved
    :return: The body of the POST request
    """

    headers = {"Content-Type": "application/json"}
    body = json.dumps(model_to_save)
    if MIDDLEWARE_ON:
        logger.info(f"Pushing {model_to_save.get('model').get('name')} middleware")
        response = requests.post(
            f"{middleware}trained_models/", headers=headers, data=body
        )
        if response.status_code != 201:
            logger.error(
                f"Something went wrong in saving the model, rollback to latest version\n {response.content}"
            )
        else:
            logger.info("Model pushed successfully")

    return body


def sync_trained_models():
    """
    Syncs the trained models from the middleware to the local server.
    First check remote trained model with their versions. If models and versions are not available,
    delete locally
    Then check for local models. If a local payload is stored, post to middleware.
    Moreover, double checks for algorithm id. If not found, updates with current algorithm id in middleware
    Finally, if a local payload is not found, delete the folder
    """
    logger.info("Syncing trained models")
    remote_trained_models = requests.get(f"{middleware}trained_models/").json()[
        "models"
    ]
    local_trained_models = list_trained_models()  # Image Paths

    for remote_trained_model in remote_trained_models:
        model_id = remote_trained_model["model"]["id"]
        model_payload = requests.get(f"{middleware}trained_models/{model_id}").json()
        for version in model_payload["versions"]:
            version_trimmed_name = version["image_path"].split("/")[-1]
            if version_trimmed_name not in local_trained_models:
                requests.delete(
                    f"{middleware}trained_models/{model_id}/?version_id={version['id']}"
                )
                logger.info(f"Deleted {model_id} from remote server")
            else:
                local_trained_models.remove(version_trimmed_name)

    for local_trained_model in local_trained_models:
        try:
            local_payload_filepath = retrieve_model_payload(local_trained_model)
            with open(local_payload_filepath, "r") as f:
                model_payload = json.load(f)
                if not model_payload.get("model").get("algorithm"):
                    algo_long_name = model_payload.get("model").get(
                        "algorithm_long_name"
                    )
                    model_payload["model"]["algorithm"] = ALGORITHM_LONG_NAME_TO_ID.get(
                        algo_long_name
                    )
                    save_model_payload(get_folder_full_path(local_trained_model), model_payload)
                post_model_to_middleware(model_payload)
        except FileNotFoundError:
            logger.error("Local Payload not found, deleting folder")
            delete_folder(get_folder_full_path(local_trained_model))

    logger.info("Sync completed")


def sync_available_algorithms():
    """
    Syncs the available algorithms from the middleware to the local server.
    """
    response = requests.get(f"{middleware}algorithms/")

    for remote_algo in response.json().get("algorithms", []):
        if remote_algo.get("name") not in ALGORITHM_SHORT_TO_LONG.keys():
            requests.delete(url=f"{middleware}algorithms/{remote_algo.get('id')}")

    for algorithm in browse_algorithms():
        long_name = algorithm["algorithm"]["name"]
        algorithm["algorithm"]["name"] = ALGORITHM_LONG_TO_SHORT[long_name]
        response = requests.post(url=f"{middleware}algorithms/", json=algorithm)

        if not response.status_code == 201:
            logger.error(f"Error syncing algorithm: {response.text}")
        else:
            algo_id = response.json().get("id")
            ALGORITHM_LONG_NAME_TO_ID[long_name] = algo_id

    logger.info("Algorithm sync completed")
