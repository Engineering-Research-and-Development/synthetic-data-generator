import os

import pytest
import yaml
from starlette.testclient import TestClient
from ..server.main import app

with open(os.path.join(os.path.dirname(__file__), 'config.yml'), 'r')  as file:
    config = yaml.safe_load(file)
    server = config["server"]
    port = config['port']


@pytest.fixture(scope="package")
def client():
    with TestClient(app=app, root_path="database", client=(server, port)) as client:
        return client