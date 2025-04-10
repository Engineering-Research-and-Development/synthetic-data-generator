import time

import requests
import pytest

from conftest import middleware, load_jsons
from algorithms import algorithms_available

url = middleware + "/sdg_input/"


@pytest.mark.dependency()
@pytest.mark.parametrize("filename,payload", load_jsons("../resources/sdg_input"))
def test_sdg_input(filename, payload, algorithms_available):
    model_id = list(algorithms_available.keys())[
        list(algorithms_available.values()).index(payload["test"])
    ]
    payload.pop("test")
    payload["ai_model"]["selected_model_id"] = model_id
    response = requests.post(url, json=payload)
    assert response.status_code == 200, (
        f"Failed on file: {filename} with status code {response.status_code} and body: {response.text}"
    )


@pytest.mark.dependency(name="test_sdg_input")
def test_check_pushed_models():
    time.sleep(10)
    response = requests.get(middleware + "/trained_models")
    json_response = response.json()
    assert len(json_response["models"]) >= 1
