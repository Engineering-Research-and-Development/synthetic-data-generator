import pytest
import requests

from src.generator.ai_lib.browse_algorithms import browse_algorithms
from .conftest import trained_models_folder, test_folder
from ..file_utils import get_all_subfolders_ids
from ..middleware_handlers import (
    # server_sync_train_data,
    sync_remote_trained,
    middleware, sync_remote_algorithm,
    # server_sync_algorithms,
)


def test_sync_train():

    sync_remote_trained(
         "trained_models/?include_version_ids=false&index_by_id=true",
        test_folder
    )
    # Now we check if the remote has the same stuff we have locally
    response = requests.get(
        f"{middleware}trained_models?include_version_ids=false&index_by_id=true"
    )
    assert response.status_code == 200
    remote_train = response.json()
    assert len(remote_train) > 0
    # We search for the names since the ids might have been changed
    for path, trained_id in get_all_subfolders_ids(trained_models_folder):
        assert remote_train.get(trained_id) is not None
        assert remote_train.pop(str(trained_id))
    # If the two match, the repo should now be empty
    assert not remote_train


def test_sync_algo():
    sync_remote_algorithm()
    response = requests.get(f"{middleware}algorithms/?include_allowed_datatypes=false&indexed_by_names=true")
    assert response.status_code == 200,print(response.content)
    remote_algos = response.json()
    assert remote_algos
    for algo in browse_algorithms():
        assert remote_algos.pop(algo['name'],None) is not None
    assert not remote_algos



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



