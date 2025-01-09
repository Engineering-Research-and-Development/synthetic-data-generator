import json
import requests

localhost = "http://127.0.0.1:8000/versions"

def test_get_all_versions():
    response = requests.get(localhost)
    assert response.status_code == 200
    versions = response.json()
    for version in versions:
        assert version["id"]
        assert version["version_name"]
        assert version["trained_model_id"]
        assert version["timestamp"]
        assert version["model_image_path"]
        assert version["training_info_id"]

def test_get_version_by_id(get_all_versions):
    for test_version in get_all_versions:
        response = requests.get(localhost + "/" + str(test_version["id"]))
        assert response.status_code == 200
        version = response.json()
        assert version["id"] == test_version["id"]
        assert version["version_name"] == test_version["version_name"]
        assert version["trained_model_id"] == test_version["trained_model_id"]
        assert version["timestamp"] == test_version["timestamp"]
        assert version["model_image_path"] == test_version["model_image_path"]
        assert version["training_info_id"] == test_version["training_info_id"]


