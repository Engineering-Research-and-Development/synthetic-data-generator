from ..middleware_handlers import load_trees
from ..middleware_handlers import middleware
import requests
import pytest

tree_trained,tree_algo = load_trees()
trained_models,algorithms = [],[]

@pytest.fixture(scope="module")
def local_repo_trees():
    global tree_trained,tree_algo
    return tree_trained,tree_algo

# Why do this? The sync operations are quite destructive (a lot of POST/DELETE based on the generator algo/trianed models
# view) for this reason, we get a copy of all the data present in the registry before the tests then we restore it.
# Basically this is a rollback
def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    global trained_models,algorithms
    data = requests.get(f"{middleware}trained_models/?include_version_ids=false&index_by_id=false").json()
    # We need to cycle this bc we need to get more infos so that the POST will work after
    for model in trained_models:
        
    algorithms = requests.get(f"{middleware}algorithms/?include_allowed_datatypes=false&indexed_by_names=true")


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    global tree_trained,tree_algo
    tree_trained.close(),tree_algo.close()
    # Restoring the model registry
    for model in trained_models:
        requests.post(f"{middleware}trained")

