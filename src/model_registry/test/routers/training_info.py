import requests
import yaml
from fastapi.testclient import TestClient
from src.model_registry.server.main import app


with open('src/model_registry/test/routers/config.yml', 'r') as file:
    config = yaml.safe_load(file)
    server = config["server"]
    port = config["port"]
endpoint = "/training_info"

client = TestClient(app, client=(server, port))

def test_get_training_info():
    response = client.get(server + endpoint + "/1")
    assert response.status_code == 200
    data = response.json()
    assert data['loss_function']
    assert data['train_loss']
    assert data['val_loss']
    assert data['train_samples']
    assert data['val_samples']
    assert data['id']