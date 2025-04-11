import time

import pytest
import requests

from conftest import middleware

url = middleware + "/trained_models/"


@pytest.mark.dependency(name="test_sdg_input")
def test_check_pushed_models():
    time.sleep(60)
    response = requests.get(url)
    json_response = response.json()
    assert len(json_response["models"]) >= 1
