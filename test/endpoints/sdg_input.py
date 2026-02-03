import copy
import requests
import pytest

from conftest import load_jsons, SERVICE_CONFIG
from trained_models import (
    check_pushed_model,
)

URL = f"{SERVICE_CONFIG.middleware}/sdg_input/"


@pytest.mark.parametrize("filename,raw_payload", load_jsons("resources/new_models"))
def test_train_sdg_input(filename, raw_payload):
    payload = copy.deepcopy(raw_payload)
    response = requests.post(URL, json=payload)

    assert response.status_code == 200, (
        f"[TRAIN] {filename} failed ({response.status_code}): {response.text}"
    )

    check_pushed_model(payload["data"]["ai_model"]["new_model_name"])
