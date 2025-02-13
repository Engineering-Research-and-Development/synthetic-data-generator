import random
from ..conftest import server,port



endpoint = "/versions"

def test_get_all_versions(client):
    response = client.get(f"{server}:{port}{endpoint}")
    assert response.status_code == 200
    random_version = random.choice(response.json())
    assert random_version['id']
    assert random_version['version_name']
    assert random_version['image_path']

def test_get_version_id(client):
    response = client.get(f"{server}:{port}{endpoint}" + "/1")
    assert response.status_code == 200
    data = response.json()
    assert data['id']
    assert data['version_name']
    assert data['image_path']

def test_get_bad_version_id(client):
    assert client.get(f"{server}:{port}{endpoint}" + "/1000").status_code == 404

