import requests
from fastapi import status

BASE_URL = "http://localhost:8001/algorithms"
algo_id = None


def test_create_new_algorithm():
    global algo_id
    payload = {
        "algorithm": {
            "name": "Test Algorithm",
            "description": "A test algorithm",
            "default_loss_function": "mse",
        },
        "datatypes": [{"type": "float", "is_categorical": False}],
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    algo_id = response.json()["id"]


def test_get_algorithm_by_id():
    algorithm_id = algo_id
    response = requests.get(f"{BASE_URL}/{algorithm_id}")
    assert response.status_code == status.HTTP_200_OK
    assert "algorithm" in response.json()
    assert "datatypes" in response.json()


def test_get_all_algorithms():
    response = requests.get(BASE_URL)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json().get("algorithms"), list)


def test_delete_algorithm():
    algorithm_id = algo_id
    response = requests.delete(f"{BASE_URL}/{algorithm_id}")
    assert response.status_code == status.HTTP_200_OK
