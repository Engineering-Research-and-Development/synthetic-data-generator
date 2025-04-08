import os
import glob
import json
import requests
import pytest

from conftest import middleware

url = middleware + "/sdg_input/"


def load_jsons():
    resources_path = "../resources"
    json_files = glob.glob(os.path.join(resources_path, "*.json"))

    jsons = []
    for json_file in json_files:
        with open(json_file) as f:
            jsons.append((json_file, json.load(f)))

    return jsons


@pytest.mark.parametrize("filename,payload", load_jsons())
def test_sdg_input(filename, payload):
    response = requests.post(url, json=payload)
    assert response.status_code == 200, (
        f"Failed on file: {filename} with status code {response.status_code} and body: {response.text}"
    )
