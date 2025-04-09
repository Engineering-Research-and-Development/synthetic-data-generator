import requests
import pytest
from conftest import middleware

@pytest.fixture(scope="module")
def algorithms_available():
    response = requests.get(middleware + "/algorithms")
    assert response.status_code == 200

    algorithms = response.json()["algorithms"]
    algorithms_available = {item.get("id"):item.get("name") for item in algorithms}
    assert len(algorithms_available)>=1
    return algorithms_available

