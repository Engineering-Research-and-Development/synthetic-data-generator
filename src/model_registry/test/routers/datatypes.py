import json

import requests
import yaml
import random

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)
    server = config["server"]
endpoint = "/datatypes"

test_datatype = {
          "type":"TestDatatype",
          "is_categorical":"false"
}



def test_get_all_datatypes():
    response = requests.get(server + endpoint)
    data = response.json()

    # Check something is returned
    assert len(data) > 0

    # Check all keys are present
    random_type = data[random.randint(0, len(data))]
    assert random_type["is_categorical"]
    assert random_type["type"]
    assert random_type["id"]

    # Check no more keys are present in the payload
    random_type.pop("is_categorical")
    random_type.pop("type")
    random_type.pop("id")

    assert len(random_type) == 0


def test_get_datatype_id():
    payload = "/1"
    response = requests.get(server + endpoint + payload)
    data = response.json()

    assert data["is_categorical"] == True
    assert data["type"] == "string"
    assert data["id"] == 1

    # Check no more keys are present in the payload
    data.pop("is_categorical")
    data.pop("type")
    data.pop("id")

    assert len(data) == 0


def test_no_datatype_id():
    payload = "/0"
    response = requests.get(server + endpoint + payload)

    assert response.status_code == 404


def test_wrong_datatype_payload():
    payload = "/wrong_payload"
    response = requests.get(server + endpoint + payload)

    assert response.status_code == 422

def test_create_datatype():
    assert requests.post(server + endpoint,json.dump(test_datatype)).status_code == 201
