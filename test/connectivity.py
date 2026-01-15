import pytest
import requests
from conftest import ServiceConfig


@pytest.mark.parametrize(
    "service_name",
    ["middleware", "couch", "generator"],
)
@pytest.mark.dependency()
def test_services_connectivity(get_services: ServiceConfig, service_name: str):
    url = getattr(get_services, service_name)
    response = requests.get(url, timeout=5)
    assert response.status_code == 200
