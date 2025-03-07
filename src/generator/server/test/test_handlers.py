import os
from copyreg import pickle
from shutil import rmtree
import pytest
import requests
import pickle
from .conftest import trained_models_folder
from ..middleware_handlers import (
    server_sync_train_data,
    sync_remote_trained,
    middleware,
    server_sync_algorithms,
)
from hashlib import sha256
from src.generator.ai_lib.browse_algorithms import browse_algorithms

test_local_algos = [
    {
        "name": "data_generator.models.keras.implementation.TabularVAE.TabularVAE_"
        + str(i),
        "default_loss_function": "ELBO LOSS",
        "description": "A Variational Autoencoder for data generation",
        "allowed_data": [
            {"data_type": "float32", "is_categorical": False},
            {"data_type": "int32", "is_categorical": False},
            {"data_type": "int64", "is_categorical": False},
        ],
    }
    for i in range(10)
]


def test_sync_remote_train(local_repo_trees):
    tree_trained, _ = local_repo_trees
    sync_remote_trained(
        tree_trained, "trained_models/?include_version_ids=false&index_by_id=true"
    )
    # Now we check if the remote has the same stuff we have locally
    response = requests.get(
        f"{middleware}trained_models?include_version_ids=false&index_by_id=true"
    )
    assert response.status_code == 200
    remote_train = response.json()
    assert len(remote_train) > 0
    # We search for the names since the ids might have been changed
    train_names = [x["name"] for x in remote_train.values()]
    for val in tree_trained.values():
        assert pickle.loads(val)["name"] in train_names


# This kind of tests should be conducted at the end since they add test data that will not work with POSTs
def test_server_sync_new_trained_data(local_repo_trees):
    tree_trained, _ = local_repo_trees
    # Creating a new folder to simulate new data
    os.makedirs(trained_models_folder + "\\100")
    assert os.path.exists(trained_models_folder + "\\100")
    with open(trained_models_folder + "\\100\\model.pickle", "wb") as handle:
        # This warning is erroneous and should be not considered
        pickle.dump({"name": "A testing name", "size": "A testing size"}, handle)
    assert os.path.exists(trained_models_folder + "\\100\\model.pickle")
    # Now we call the handler
    server_sync_train_data(tree_trained, "test\\saved_models\\trained_models")
    # We check if the handler correctly added the new folder to the tree
    assert tree_trained.get(100)
    # Cleanup
    rmtree(trained_models_folder + "\\100")
    assert not os.path.exists(trained_models_folder + "\\100")

@pytest.mark.skip(reason="Import error by AI lib"
                         "by calling browse_algorithms(), could not execute this test")
def test_server_sync_algo(local_repo_trees):
    _, tree_algo = local_repo_trees
    # Since the algorithms are passed by the generator we only check if they are being correctly inserted in the tree
    gen_algos = [x for x in browse_algorithms()]
    for algo in gen_algos:
        key = sha256(algo['name'].encode('utf-8')).hexdigest()[:16]
        assert tree_algo.get(key)

@pytest.mark.skip(reason="Import error by AI lib"
                         "by calling browse_algorithms(), could not execute this test")
def test_intersec_and_integrate_remote_data():
    pass



