import json
import os
import pickle
from pathlib import Path

import requests
from bplustree import BPlusTree, StrSerializer, IntSerializer
from requests.exceptions import RequestException

from ai_lib.Dataset import Dataset
from ai_lib.Exceptions import ModelException
from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from server.file_utils import MODEL_FOLDER
from server.file_utils import create_server_repo_folder_structure

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


def model_to_middleware(model: UnspecializedModel, data: Dataset):
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
    tree_algorithms,tree_trained_models = load_trees()
    # 1.  Analyse the existing folders, looking for trained_models models *
    mock_generator_trained_models = []
    server_sync_trained(tree_trained_models,mock_generator_trained_models)
    # 2. Synchronize (POST/DELETE) with the middleware for existing trained_models models
    remote_sync(tree_trained_models,'trained_models/?include_version_ids=False&index_by_id=True')
    # 3.  Analyse the existing folders, looking for algorithms
    # This is mock data at the moment
    mock_generator_algorithms = [{'name':'System_' + str(i), 'description': 'A description'
                                     , 'default_loss_function':'A loss function','folder_path':'server/saved_models/algorithms/i'} for i in range(10)]
    # 3.a We sync with local algorithm that the generator has
    server_sync_algorithms(tree_algorithms,mock_generator_algorithms)
    # 4. Synchronize (POST/DELETE) with the middleware for existing algorithms
    remote_sync(tree_algorithms,'algorithms/?include_allowed_datatypes=False&indexed_by_names=True')


### Methods for dealing with server saved models
def load_trees(tree_trained_order: int = 341,
               trained_key_size: int = 4,
               tree_algo_order: int = 108,
               algo_key_size: int = 32) -> tuple[BPlusTree, BPlusTree]:
    """
    This function finds looks for the B+Trees' pickle inside the server folder. If found, it will load them and return the
    reference of them, otherwise it will create them from scratch and return them.
    :param: tree_trained_order The maximum number of children per internal node for the tree of trained models. Since we
    will use ints for the keys, the optimal parameter is 341 which is the default value
    :param: trained_key_size The key size in bytes of each node in the tree of the trained models. Using ints, the
    key size is 4 bytes, which is the default value
    :param: tree_algo_order The maximum number of children per internal node for the tree of algorithms. Since we
    will use strings for the keys, the optimal parameter is 108 which is the default value
    :param: algo_key_size The key size in bytes of each node in the tree of the algorithms. Using medium strings as keys, the
    key size is 32 bytes, which is the default value
    :return: A tuple containing respectively the B+Tree for algorithms and trained models
    """
    create_server_repo_folder_structure()
    tree_trained_models = BPlusTree(
        Path(os.path.dirname(os.path.abspath(__file__)) + "\\saved_models\\trained_models\\bplus_tree.db"),
        order=tree_trained_order, key_size=trained_key_size, serializer=IntSerializer()
    )
    tree_algo = BPlusTree(
        Path(os.path.dirname(os.path.abspath(__file__)) + "\\saved_models\\algorithms\\bplus_tree.db")
        , order=tree_algo_order, key_size=algo_key_size,serializer=StrSerializer()
    )
    return tree_trained_models, tree_algo


def server_sync_trained(repo_tree: BPlusTree, trained_models: list) -> None:
    """
    This function given the algorithms that the generator currently implements, it fills the tree up with the data
    so that the server repo is up to date with the generator work.
    :return:
    """
    # Since each algorithm is different from each other, we can use as key the algorithm name
    zipped_hashed_names  = [(int(elem['id']),pickle.dumps(elem)) for elem in trained_models]
    zipped_hashed_names.sort(key=lambda tup: tup[0])
    # This is slower, but we have more control on the tree
    for key, value in zipped_hashed_names:
        repo_tree.insert(key, value, replace=True)


def server_sync_algorithms(repo_tree: BPlusTree, generator_algorithms: list) -> None:
    """
    This function given the algorithms that the generator currently implements, it fills the tree up with the data
    so that the server repo is up to date with the generator work.
    :return:
    """
    # Since each algorithm is different from each other, we can use as key the algorithm name
    zipped  = [(elem['name'],pickle.dumps(elem)) for elem in generator_algorithms]
    zipped.sort(key=lambda tup: tup[0])
    # This is slower, but we have more control on the tree
    for key,value in zipped:
        repo_tree.insert(key,value,replace=True)


def remote_sync(local_repo: BPlusTree,endpoint):
    """
    This function given the algorithms in the repo it syncs with the algorithm in the model registry. The model registry
    needs to reflect the algorithm that the generator has.
    :return:
    """
    root_endpoint = endpoint[:str.index(endpoint,'/')]
    # Checkout all algorithms from repo, this return a dictionary containing the unique names from the registry
    response = requests.get(f"{middleware}{endpoint}")
    if response.status_code == 404:
        raise TimeoutError("Could not reach middleware for synchronization!")
    remote_data = response.json()
    # We scan all the local algorithms for the remote ones, if found we delete them otherwise we create them
    intersec_and_integrate_remote_data(local_repo, remote_data, root_endpoint)
    # The rest of the remote are the ones that are not implemented by the generator, hence they must be deleted
    remove_remote_data_not_present(remote_data,root_endpoint)

def intersec_and_integrate_remote_data(local_repo: BPlusTree,remote_data: dict,root_endpoint: str):
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
            response = requests.post(f"{middleware}/{root_endpoint}/", json=pickle.loads(value))
            assert response == 200, print(response.content)
        else:
            remote_data.pop(key)

def remove_remote_data_not_present(remote_data: dict,root_endpoint: str):
    for data in remote_data:
        response = requests.delete(f"{middleware}/{root_endpoint}/{data['id']})")
        assert response == 200, print(response.content)