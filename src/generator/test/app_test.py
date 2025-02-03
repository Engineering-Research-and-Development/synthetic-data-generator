import json
import requests

train_correct = "train_test.json"
infer_correct_1 = "infer_test.json"
infer_correct_2 = "infer_test_nodata.json"
out_file = "test_results.txt"


def test_train():
    endpoint = "http://localhost:8010/train"
    with open(train_correct, 'r') as file:
        data = json.load(file)
    response = requests.post(endpoint, json=data)
    assert response.status_code == 200


def test_infer():
    endpoint = "http://localhost:8010/infer"
    with open(infer_correct_1, 'r') as file:
        data = json.load(file)
    response = requests.post(endpoint, json=data)
    assert response.status_code == 200
    assert response.json()["result_data"] is not None
    assert response.json()["metrics"] is not None


def test_infer_nodata():
    endpoint = "http://localhost:8010/infer"
    with open(infer_correct_2, 'r') as file:
        data = json.load(file)
    response = requests.post(endpoint, json=data)
    assert response.status_code == 200
    assert response.json()["result_data"] is not None
    assert response.json()["metrics"] is not None


def test_infer_wrong():
    endpoint = "http://localhost:8010/infer"
    with open(train_correct, 'r') as file:
        data = json.load(file)
    response = requests.post(endpoint, json=data)
    assert response.status_code == 500

