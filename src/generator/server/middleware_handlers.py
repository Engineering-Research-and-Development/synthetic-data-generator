import json
import os
import pickle
from copy import deepcopy

import requests
from requests.exceptions import RequestException

from ai_lib.Exceptions import ModelException
from ai_lib.NumericDataset import NumericDataset
from ai_lib.browse_algorithms import browse_algorithms
from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from server.file_utils import MODEL_FOLDER, get_all_subfolders_ids, does_pickle_file_exists
from server.validation_schema import DatasetIn

middleware = os.environ.get("MIDDLEWARE_URL", "http://sdg-middleware:8001/")


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


def model_to_middleware(model: UnspecializedModel, data: NumericDataset):
    feature_list = data.parse_data_to_registry()
    training_info = model.training_info.to_dict()
    model_image = model.model_filepath # Qui ci passi il tuo save path. -> Prima crei couch entry vuota con ID, dopo usi ID per creare cartella
    model_version = model.check_folder_latest_version(MODEL_FOLDER) # Da riscrivere per gestire le cartelle con le versioni
    # Io facevo Algorithm_Name__Model_Name:model_version
    # Ti consiglio di fare id:version_number
    version_info = {"version_name": model_version, "model_image_path": model_image} # Gestione versioni come sopra
    trained_model_misc = {
        "name": model.model_name,
        "size": model.self_describe().get("size", "Not Available"),
        "input_shape": str(model.input_shape),
        "algorithm_name": model.self_describe().get("name", None),
    }

    model_to_save = {
        "trained_model": trained_model_misc,
        "version": version_info,
        "training_info": training_info,
        "feature_schema": feature_list,
    }

    headers = {"Content-Type": "application/json"}
    body = json.dumps(model_to_save)
    try:
        response = requests.post(
            f"{middleware}trained_models/", headers=headers, data=body
        )
        if response.status_code > 300:
            raise ModelException(
                "Something went wrong in saving the model, rollback to latest version"
            )
    except RequestException:
        raise ModelException(
            "Impossible to reach Model Repository, rollback to latest version"
        )

def server_startup():
    # 1. Sync with any new implemented trained models and Sync with remote
    sync_remote_trained()
    # 1. Sync with any new implemented algorithms and Sync with remote
    sync_remote_algorithm()


def sync_remote_trained(endpoint: str,folder: str):
    root_endpoint = endpoint[:str.index(endpoint, '/')]
    response = requests.get(f"{middleware}{endpoint}")
    if response.status_code == 404:
        raise TimeoutError("Could not reach middleware for synchronization!")
    remote_data = response.json()
    for path,trained_id in get_all_subfolders_ids(f"{folder}\\saved_models\\trained_models"):
        if remote_data.get(trained_id) is None:
            with open(path + "\\model.pickle",'rb') as file:
                payload = pickle.load(file)
            f_payload = format_trained_model_for_post(deepcopy(payload))
            response = requests.post(f"{middleware}/{root_endpoint}", json=f_payload)
            assert response.status_code == 201, print(response.content)
            del f_payload
            # Now we must update the model id locally since it has been created in the repo with a new id
            update_trained_model(payload,trained_id,response.json()['id'],folder)
        else:
            remote_data.pop(trained_id)
    # Here we remove the remote data
    for key in remote_data.keys():
        response = requests.delete(f"{middleware}/{root_endpoint}/{key}")
        assert response.status_code == 200, print(response.content)

def format_trained_model_for_post(model: dict) -> dict[str,str | int]:
    model.update({'trained_model': {'name': model['name'], 'dataset_name': model['dataset_name'],
                                    'size': model['size'], 'input_shape': model['input_shape'],
                                    'algorithm_id': model['algorithm_id']}})
    model.pop('id')
    model.pop('name')
    model.pop('dataset_name')
    model.pop('size')
    model.pop('input_shape')
    model.pop('algorithm_id')
    model.pop('algorithm_name')
    model.update({'version': model['versions'][0]['version']})
    model.update({'training_info': model['versions'][0]['training_info']})
    model.pop('versions')
    return model

def update_trained_model(tr_data: dict,old_id: int,new_id: int,folder: str):
    # Modify the payload
    tr_data['id'] = new_id
    # Dump the model to the folder
    with open(os.path.abspath(f'{folder}\\saved_models\\trained_models\\{old_id}\\model.pickle'),'wb') as file:
        pickle.dump(tr_data,file)
    # Rename the folder
    os.rename(f'{folder}\\saved_models\\trained_models\\{old_id}',f'{folder}\\saved_models\\trained_models\\{new_id}')

def save_new_trained_model(model_dict: dict,
                           dataset_name: str,
                           size: str,
                           algo_id: int,
                           tr_info: str,
                           feature_schema: str):
    image_path = model_dict['image']
    tr_name = model_dict['model_name']
    input_shape = model_dict['input_shape']

def create_feature_schema(features_in: list[DatasetIn]):
    pass

def sync_remote_algorithm():
    # Since the generator offers a method that lists all the implemented algorithms we only
    # need to do a sync with the remote repository
    response = requests.get(f'{middleware}algorithms/?include_allowed_datatypes=true&indexed_by_names=true')
    if response.status_code != 200:
        raise TimeoutError("Could not reach middleware for algorithms sync! Server returned the following"
                           " code",response.status_code)
    remote_algorithms = response.json()
    for algorithm in browse_algorithms():
        if remote_algorithms.get(algorithm['name']) is None:
            f_algorithm = format_algorithm_for_post(deepcopy(algorithm))
            response = requests.post(f'{middleware}algorithms/', json=f_algorithm)
            # This means that the datatype is not present and the specific datatype must be added
            if response.status_code == 400 and response.json()['datatype'] is not None:
                # We search it in the datatypes that we are passing to the post
                to_add = response.json()['datatype']
                for datatype in f_algorithm['allowed_data']:
                    if datatype['datatype'] == to_add['type'] and datatype['is_categorical'] == to_add['is_categorical']:
                        response = requests.post(f"{middleware}datatypes/",json=datatype)
                        assert response.status_code == 201,print(response.content)
                # Now we retry the creation
                response = requests.post(f'{middleware}algorithms/', json=f_algorithm)
                assert response.status_code == 201,print(response.content)
            assert response.status_code == 201,print(response.content)
            del f_algorithm
        else:
            remote_algorithms.pop(algorithm['name'])

    # Now we delete all the rest of the stuff from the repo
    for key,val in remote_algorithms.items():
        response = requests.delete(f'{middleware}algorithms/{val["id"]}')
        assert response.status_code == 200,print(response.content)

def format_algorithm_for_post(algorithm: dict) -> dict:
    algorithm.update({'algorithm':
        {
        'name':algorithm['name'],
        'default_loss_function': algorithm['default_loss_function'],
        'description': algorithm['description'],
        }
    })
    # Changing the key data_type to datatype for each obj in 'allowed_data'
    for data in algorithm['allowed_data']:
        data.update({'datatype':data['data_type']})
        data.pop('data_type')
    algorithm.pop('name')
    algorithm.pop('default_loss_function')
    algorithm.pop('description')
    return algorithm

def get_algorithm_path(algorithm: dict,root_folder: str) -> str | None:
    # Check if present in the model registry
    response = requests.get(f"{middleware}/algorithms/{algorithm['algorithm_name']}")
    if response.status_code == 404:
        return None
    # Now we get the id, and we check if it is present also locally and we see if the data is passed correctly
    algo_id = response.json()['id']
    if does_pickle_file_exists(root_folder,algo_id):
        # Load model information and check consistency
        with open(os.path.join(root_folder,f"saved_models\\{algo_id}\\model.pickle"),'rb') as file:
            model = pickle.load(file)
        if not model['name'] == algorithm['model']['algorithm_name']:
            return None
    else:
        return None
    return os.path.join(root_folder,f"\\saved_models\\algorithms\\{algo_id}")

def fetch_model_save_path(model_dict: dict):
    pass




