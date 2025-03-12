import os
import pickle
import random
from copy import deepcopy
from shutil import rmtree

import requests

from ..middleware_handlers import middleware

# Creating temp files for testing server sync methods
test_folder = os.path.dirname(os.path.abspath(__file__))
trained_models_folder = test_folder + "\\saved_models\\trained_models"
algorithms_folder = test_folder + "\\saved_models\\algorithms"
# Creating test folder structure for the B+Trees
if not os.path.isdir(test_folder + "\\saved_models"):
    os.makedirs(test_folder + "\\saved_models")
if not os.path.isdir(trained_models_folder):
    os.makedirs(trained_models_folder)
if not os.path.isdir(algorithms_folder):
    os.makedirs(algorithms_folder)

trained_models, algorithms = [], []

# Why do this? The sync operations are quite destructive (a lot of POST/DELETE based on the generator algo/trianed models
# view) for this reason, we get a copy of all the data present in the registry before the tests then we restore it.
# Basically this is a rollback
def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    global trained_models, algorithms
    data = requests.get(
        f"{middleware}trained_models/?include_version_ids=false&index_by_id=false"
    ).json()
    # We need to cycle this bc we need to get more infos so that the POST will work after
    for model in data:
        trained_models.append(
            requests.get(
                f"{middleware}trained_models/{model['id']}"
                f"?include_versions=true&include_training_info=true"
            ).json()
        )

    algorithms = requests.get(
        f"{middleware}algorithms/?include_allowed_datatypes=true&indexed_by_names=false"
    ).json()

    assert len(trained_models) != 0
    assert len(algorithms) != 0

    to_add = []
    # We make some dirs and mock data in the files
    for i in range(1, 6):
        os.makedirs(test_folder + f"\\saved_models\\trained_models\\{i}")
        mock_train = {
            "name": "TrainedModel_" + str(i),
            "dataset_name": "Dataset_" + str(i),
            "size": "30MB",
            "input_shape": "(2,3,4)",
            "algorithm_id": random.choice(algorithms)["id"],
            "id": i,
            "algorithm_name": random.choice(algorithms)["name"],
            "versions": [
                {
                    "version": {
                        "version_name": "v1.0",
                        "image_path": "/models/unique_model_0.h5",
                        "id": 1,
                    },
                    "training_info": {
                        "loss_function": "LossFunction_0",
                        "train_loss": 0.05,
                        "val_loss": 0.1,
                        "train_samples": 10,
                        "val_samples": 5,
                        "id": 1,
                        "model_version_id": 1,
                    },
                }
            ],
            "feature_schema": [
                {
                    "feature_name": "Feature_0",
                    "feature_position": 1,
                    "is_categorical": "true",
                    "datatype": "DataType_0",
                }
            ],
        }
        with open(
            test_folder + f"\\saved_models\\trained_models\\{i}\\model.pickle", "wb"
        ) as file:
            pickle.dump(mock_train, file)
        # to_add.append((i, pickle.dumps(mock_train)))
    # # Now we add them as startup training data
    # tree_trained.batch_insert(to_add)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    # First we delete everything
    response = requests.get(
        f"{middleware}trained_models/?include_version_ids=false&index_by_id=false"
    )
    assert response.status_code == 200
    remote_trains = response.json()
    for train in remote_trains:
        assert (
            requests.delete(f"{middleware}trained_models/{train['id']}").status_code
            == 200
        )

    response = requests.get(f"{middleware}algorithms/")
    assert response.status_code == 200
    remote_algos = response.json()
    for algo in remote_algos:
        assert (
            requests.delete(f"{middleware}algorithms/{algo['id']}").status_code == 200
        )

    # Rolling back algorithms
    algo_to_post = deepcopy(algorithms)
    for algo in algo_to_post:
        # Changing the data so that we can make the POST
        algo.update(
            {
                "algorithm": {
                    "name": algo["name"],
                    "description": algo["description"],
                    "default_loss_function": algo["default_loss_function"],
                    "id": algo["id"],
                }
            }
        )
        algo.pop("name")
        algo.pop("description")
        algo.pop("default_loss_function")
        algo.pop("id")
        response = requests.post(f"{middleware}algorithms/", json=algo)
        assert response.status_code == 201, print(response.content)

    # Rolling back trained models
    # Getting the inserted algorithms since now the ids have changed but the name are the same
    algo_dict = requests.get(
        f"{middleware}algorithms/?include_allowed_datatypes=false&indexed_by_names=True"
    ).json()
    trained_models_to_post = deepcopy(trained_models)
    for model in trained_models_to_post:
        # Changing the data so that we can make the POST
        model.update(
            {
                "trained_model": {
                    "name": model["name"],
                    "dataset_name": model["dataset_name"],
                    "size": model["size"],
                    "input_shape": model["input_shape"],
                    "algorithm_id": algo_dict.get(model["algorithm_name"])["id"],
                }
            }
        )
        model.pop("name")
        model.pop("dataset_name")
        model.pop("size")
        model.pop("input_shape")
        model.pop("algorithm_id")
        model.pop("algorithm_name")
        model["versions"] = model["versions"][0]
        model.update({"training_info": model["versions"]["training_info"]})
        model.update({"version": model["versions"]["version"]})
        model.pop("versions")
        response = requests.post(f"{middleware}trained_models/", json=model)
        assert response.status_code == 201, print(response.content)

    # Checking if the rollback is successful
    remote_train_models = requests.get(
        f"{middleware}trained_models/?include_version_ids=false&index_by_id=false"
    ).json()
    remote_train_models_names = [x["name"] for x in remote_train_models]
    for model in trained_models:
        assert model["name"] in remote_train_models_names
    remote_algorithms = requests.get(
        f"{middleware}algorithms/?include_allowed_datatypes=true&indexed_by_names=true"
    ).json()
    for algo in algorithms:
        assert remote_algorithms.get(algo["name"])

    # Deleting temp files for server sync
    # Files cleanup
    rmtree(test_folder + "\\saved_models")
    assert not os.path.isdir(test_folder + "\\saved_models")
