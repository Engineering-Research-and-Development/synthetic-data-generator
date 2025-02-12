import pytest
import yaml
from starlette.testclient import TestClient
from src.model_registry.server.main import app

with open('src/model_registry/test/routers/config.yml', 'r') as file:
    config = yaml.safe_load(file)
    server = config["server"]
    port = config['port']


@pytest.fixture(scope="package")
def client():
    with TestClient(app, client=(server, port)) as client:
        return client