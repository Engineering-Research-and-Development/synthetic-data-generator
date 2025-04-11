import requests
import pytest
from conftest import middleware

url = middleware + "/algorithms/"


@pytest.fixture(scope="module")
def algorithms_available():
    response = requests.get(url)
    algorithms = response.json()["algorithms"]
    algorithms_available = {item.get("id"): item.get("name") for item in algorithms}

    return algorithms_available
