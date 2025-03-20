import os.path
from pathlib import Path

import requests

from ai_lib.browse_algorithms import browse_algorithms
from server.test.conftest import test_folder
from server.middleware_handlers import (
    sync_remote_trained,
    middleware,
    sync_remote_algorithm,
)

generator_url = os.environ.get("GENERATOR_URL", "http://generator:8010/")


def test_sync_train():
    sync_remote_trained("trained_models/image-paths/", test_folder)
    # We just need to check that the folders created by conftest are not present anymore since they are not in the repo
    path = os.path.join(test_folder, Path("saved_models/trained_models"))
    assert not os.path.exists(f"{path}\\1")
    assert not os.path.exists(f"{path}\\2")
    assert not os.path.exists(f"{path}\\3")
    assert not os.path.exists(f"{path}\\4")
    assert not os.path.exists(f"{path}\\5")


def test_sync_algo():
    sync_remote_algorithm()
    response = requests.get(
        f"{middleware}algorithms/?include_allowed_datatypes=false&indexed_by_names=true"
    )
    assert response.status_code == 200, print(response.content)
    remote_algos = response.json()
    assert remote_algos
    for algo in browse_algorithms():
        assert remote_algos.pop(algo["name"], None) is not None
    assert not remote_algos
