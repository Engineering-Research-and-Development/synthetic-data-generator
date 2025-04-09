import pytest
import requests
from conftest import middleware, couch, generator

@pytest.mark.parametrize("url", [middleware, couch, generator])
@pytest.mark.dependency()
def test_services_connectivity(url):
    response = requests.get(url)
    assert response.status_code == 200
