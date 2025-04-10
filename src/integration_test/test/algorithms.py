import requests
import pytest
from conftest import middleware, load_jsons

url = middleware + "/algorithms/"


@pytest.fixture(scope="module")
def algorithms_available():
    response = requests.get(url)
    assert response.status_code == 200

    algorithms = response.json()["algorithms"]
    algorithms_available = {item.get("id"): item.get("name") for item in algorithms}
    assert len(algorithms_available) >= 1
    return algorithms_available


def test_algorithms_available():
    response = requests.get(url)
    assert response.status_code == 200

    algorithms = response.json()["algorithms"]
    algorithms_available = {item.get("id"): item.get("name") for item in algorithms}
    assert len(algorithms_available) >= 1


@pytest.mark.dependency()
@pytest.mark.parametrize("filename,payload", load_jsons("../resources/algorithms"))
def test_post_algorithms(filename, payload, algorithms_available):
    response = requests.post(url, json=payload)
    assert response.status_code == 201, (
        f"Failed on file: {filename} with status code {response.status_code} and body: {response.text}"
    )


@pytest.mark.dependency(depends=["test_post_algorithms", "test_sdg_input"])
def test_get_algorithm_id(algorithms_available):
    algorithm_id = list(algorithms_available.keys())[0]
    response = requests.get(f"{url}{algorithm_id}")
    assert response.status_code == 200


@pytest.mark.dependency(name="test_post_algorithms")
def test_del_algorithm(algorithms_available):
    algorithm_id = list(algorithms_available.keys())[0]
    response = requests.delete(f"{url}{algorithm_id}")
    assert response.status_code == 200
