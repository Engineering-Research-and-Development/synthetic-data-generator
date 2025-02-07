import json
import requests
import yaml
import random

with open('src/model_registry/test/routers/config.yml', 'r') as file:
    config = yaml.safe_load(file)
    server = config["server"]

endpoint = "/versions"

def test_get_all_versions():
    response = requests.get(server + endpoint)
    assert response.status_code == 200
    random_version = random.choice(response.json())
    assert random_version['id']
    assert random_version['version_name']
    assert random_version['image_path']


def test_get_version_id():
    response = requests.get(server + endpoint + "/1")
    assert response.status_code == 200
    data = response.json()
    assert data['id']
    assert data['version_name']
    assert data['image_path']

def test_get_bad_version_id():
    assert requests.get(server + endpoint + "/1000").status_code == 404

def test_create_version():
    pass
