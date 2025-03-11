import json
import os
import pickle
from pathlib import Path

import requests
from bplustree import BPlusTree, StrSerializer, IntSerializer
from requests.exceptions import RequestException

from ai_lib.NumericDataset import NumericDataset
from ai_lib.Exceptions import ModelException
from ai_lib.browse_algorithms import browse_algorithms
from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from server.file_utils import MODEL_FOLDER
from server.file_utils import create_server_repo_folder_structure,get_all_folder_content_as_dict
from hashlib import sha256


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
    training_info = model._training_info.to_dict()
    model_image = model.model_filepath
    model_version = model.check_folder_latest_version(MODEL_FOLDER)
    version_info = {"version_name": model_version, "model_image_path": model_image}
    trained_model_misc = {
        "name": model._model_name,
        "size": model.self_describe().get("size", "Not Available"),
        "input_shape": str(model._input_shape),
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
    # Pre-work: we fetch the B+Trees for algorithms and trained models
    tree_trained_models,tree_algorithms = load_trees_from_disk()
    # 1. Sync with any new implemented trained models
    server_sync_train_data(tree_trained_models,'./saved_models/trained_models')
    # 2. Sync with remote
    sync_remote_trained(tree_trained_models,'trained_models/?include_version_ids=false&index_by_id=true')
    # 3. Sync with any new implemented algorithms
    server_sync_algorithms(tree_algorithms,'./saved_models/algorithms')
    # 4. Sync with remote algorithms
    sync_remote_algorithms(tree_algorithms,'algorithms/?include_allowed_datatypes=true&indexed_by_names=true')






### Methods for dealing with server saved models
def load_trees_from_disk(tree_trained_order: int = 341,
               trained_key_size: int = 4,
               tree_algo_order: int = 170,
               algo_key_size: int = 16) -> tuple[BPlusTree, BPlusTree]:
    """
    This function finds looks for the B+Trees' pickle inside the server folder. If found, it will load them and return the
    reference of them, otherwise it will create them from scratch and return them.
    :param: tree_trained_order The maximum number of children per internal node for the tree of trained models. Since we
    will use ints for the keys, the optimal parameter is 341 which is the default value
    :param: trained_key_size The key size in bytes of each node in the tree of the trained models. Using ints, the
    key size is 4 bytes, which is the default value
    :param: tree_algo_order The maximum number of children per internal node for the tree of algorithms. Since we
    will use medium strings (16 char in length) for the keys, the optimal parameter is 170 which is the default value
    :param: algo_key_size The key size in bytes of each node in the tree of the algorithms. Using medium strings as keys, the
    key size is 32 bytes, which is the default value
    :return: A tuple containing respectively the B+Tree for algorithms and trained models
    """
    create_server_repo_folder_structure()
    root_file = os.path.dirname(os.path.abspath(__file__))
    tree_trained_models = BPlusTree(
        Path(root_file + "/saved_models/trained_models/bplus_tree.db"),
        order=tree_trained_order, key_size=trained_key_size, serializer=IntSerializer()
    )
    tree_algo = BPlusTree(
        Path(root_file + "/saved_models/algorithms/bplus_tree.db")
        , order=tree_algo_order, key_size=algo_key_size,serializer=StrSerializer()
    )
    return tree_trained_models, tree_algo

def server_sync_train_data(local_tree: BPlusTree,folder_path: str):
    """
    This function given a folder path it checks if the data locally present is already present in the Bplustree,
    otherwise it adds it
    :param local_tree: A Bplustree that keeps track of the data, and it's position
    :param folder_path: The folder path where to look the data for
    :return:
    """
    # We fetch all the contents of the folder
    # TODO: There should be a data structure that keeps track of any new folders instead of traversing all
    #  the old ones
    folder_data = get_all_folder_content_as_dict(folder_path,cast_key_as_int=True)
    if not folder_data:
        return
    for key,value in local_tree.items():
        if folder_data.get(key) is not None:
            folder_data.pop(key)
    # Folder data will have all the model folders that are not present in the BplusTree
    insert_saved_trained_model_folders(local_tree,folder_data)


def insert_saved_trained_model_folders(repo_tree: BPlusTree, trained_folders: dict) -> None:
    """
    This function given the trained model's folders found by the server, it fills the tree up with the data
    so that the server repo is up to date with the generator work.
    :return:
    """
    # Since each algorithm is different from each other, we can use as key the name of the folder which is the
    # trained model id
    zipped_keys  = [(int(folder),pickle.dumps(data)) for folder,data in trained_folders.items()]
    zipped_keys.sort(key=lambda tup: tup[0])
    for key,val in zipped_keys:
        repo_tree.insert(key,val)


def sync_remote_trained(local_repo: BPlusTree,endpoint):
    """
    This function given the algorithms in the repo it syncs with the algorithm in the model registry. The model registry
    needs to reflect the algorithm that the generator has.
    :return:
    """
    root_endpoint = endpoint[:str.index(endpoint,'/')]
    # Checkout all the data from the repo
    response = requests.get(f"{middleware}{endpoint}")
    if response.status_code == 404:
        raise TimeoutError("Could not reach middleware for synchronization!")
    remote_data = response.json()
    intersec_and_integrate_remote_trained_data(local_repo, remote_data, root_endpoint)

def intersec_and_integrate_remote_trained_data(local_repo: BPlusTree,remote_data: dict,root_endpoint: str):
    """
    This function operates the set operation of intersection between the local data of the generator and the remote
    data. After that, it creates new data in the remote repository does not contain local data.
    :param local_repo: The local elements that the generator implements
    :param remote_data: The remote data that the repository has
    :param root_endpoint: The endpoint where to request the remote data to
    :return:
    """
    for key,value in local_repo.items():
        if remote_data.get(key) is None:
            payload = pickle.loads(value)
            payload = format_saved_trained_model(payload)
            response = requests.post(f"{middleware}/{root_endpoint}", json=payload)
            assert response.status_code == 201, print(response.content)
        else:
            remote_data.pop(key)
    # Here we remove the remote data
    for key in remote_data.keys():
        response = requests.delete(f"{middleware}/{root_endpoint}/{key}")
        assert response.status_code == 200, print(response.content)

def format_saved_trained_model(model: dict) -> dict[str,str | int]:
    print(model)
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

def server_sync_algorithms(local_tree: BPlusTree):
    # We check if the algorithms passed by the generator are present in the tree
    # https://stackoverflow.com/questions/19962424/probability-of-collision-with-truncated-sha-256-hash
    # https://en.wikipedia.org/wiki/Birthday_problem#Probability_table
    # This is very important and should be considered if the system is then developed
    # For a toy example this should be enough, since system algorithms should not be a lot
    # If the algorithms are more than 7.200.000.000 then there is a probability of
    # a collision of 75% the keying to fail to produce a collision-free key
    for algorithm in browse_algorithms():
        key = sha256(algorithm['name'].encode('utf-8')).hexdigest()[:16]
        if local_tree.get(key) is None:
            local_tree.insert(key,pickle.dumps(algorithm))

def sync_remote_algorithms(repo_tree: BPlusTree,endpoint: str):
    root_endpoint = endpoint[:str.index(endpoint,'/')]
    # Checkout all the data from the repo
    response = requests.get(f"{middleware}{endpoint}")
    if response.status_code == 404:
        raise TimeoutError("Could not reach middleware for synchronization!")
    remote_data = response.json()
    intersec_and_integrate_remote_algos(repo_tree, remote_data, root_endpoint)


def intersec_and_integrate_remote_algos(repo_tree: BPlusTree,remote_data: dict,root_endpoint: str):
    """
    This function operates the set operation of intersection between the local data of the generator and the remote
    data. After that, it creates new data in the remote repository does not contain local data.
    :param repo_tree: The local elements that the generator implements
    :param remote_data: The remote data that the repository has
    :param root_endpoint: The endpoint where to request the remote data to
    :return:
    """
    for key,value in remote_data.items():
        # Calculate hash
        key_hash = sha256(key.encode('utf-8')).hexdigest()[:16]
        # Delete every algorithm that is not present locally
        if repo_tree.get(key_hash) is None:
            response = requests.delete(f"{middleware}/{root_endpoint}/{value['id']})")
            assert response.status_code == 200, print(response.content)

    # This is inefficient but it is the only way to add non-present models
    for value in repo_tree.values():
        value = pickle.loads(value)
        response = requests.get(f"{middleware}/{root_endpoint}/{value['name']})")
        if response.status_code == 404:
            requests.post(f"{middleware}/{root_endpoint}/",json=value)
        assert response == 200, print(response.content)



