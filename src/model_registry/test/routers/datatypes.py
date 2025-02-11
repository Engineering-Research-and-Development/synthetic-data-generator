import yaml
import random
from starlette.testclient import TestClient
from src.model_registry.server.main import app

with open('src/model_registry/test/routers/config.yml', 'r') as file:
    config = yaml.safe_load(file)
    server = config["server"]
    port = config['port']
endpoint = "/datatypes"

test_datatype = {
          "type":"TestDatatype",
          "is_categorical":"false"
}

client = TestClient(app, client=(server, port))


def test_get_all_datatypes():
    response = client.get(endpoint)
    assert response.status_code == 200
    data = response.json()

    # Check something is returned
    assert len(data) > 0

    # Check all keys are present
    random_type = random.choice(data)
    assert random_type["is_categorical"] is not None
    assert random_type["type"]
    assert random_type["id"]

    # Check no more keys are present in the payload
    random_type.pop("is_categorical")
    random_type.pop("type")
    random_type.pop("id")

    assert len(random_type) == 0


def test_get_datatype_id():
    payload = "/1"
    response = client.get(server + endpoint + payload)
    data = response.json()

    assert data["is_categorical"] is not None
    assert data["type"]
    assert data["id"]

    # Check no more keys are present in the payload
    data.pop("is_categorical")
    data.pop("type")
    data.pop("id")

    assert len(data) == 0


def test_no_datatype_id():
    payload = "/0"
    response = client.get(server + endpoint + payload)

    assert response.status_code == 404


def test_wrong_datatype_payload():
    payload = "/wrong_payload"
    response = client.get(server + endpoint + payload)

    assert response.status_code == 422

def test_create_datatype():
    assert client.post(server + endpoint,json=test_datatype).status_code == 201
