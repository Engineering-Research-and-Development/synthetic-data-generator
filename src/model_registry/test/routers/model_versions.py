import yaml
import random
from starlette.testclient import TestClient
from src.model_registry.server.main import app

with open('src/model_registry/test/routers/config.yml', 'r') as file:
    config = yaml.safe_load(file)
    server = config["server"]
    port = config['port']

endpoint = "/versions"

def test_get_all_versions():
    with TestClient(app, client=(server, port)) as client:
        response = client.get(server + endpoint)
        print(response.json())
        assert response.status_code == 200
        random_version = random.choice(response.json())
        assert random_version['id']
        assert random_version['version_name']
        assert random_version['image_path']


# def test_get_version_id():
#     with TestClient(app, client=(server, port)) as client:
#         response = client.get(server + endpoint + "/1")
#         assert response.status_code == 200
#         data = response.json()
#         assert data['id']
#         assert data['version_name']
#         assert data['image_path']
#
# def test_get_bad_version_id():
#     with TestClient(app, client=(server, port)) as client:
#         assert client.get(server + endpoint + "/1000").status_code == 404
#
# def test_create_version():
#     pass
