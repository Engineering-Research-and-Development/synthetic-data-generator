import json
import requests

local_host = "http://127.0.0.1:8000/datatypes"

test = {
          "type":"string",
          "is_categorical":"false"
}

def test_get_all_datatypes():
    response = requests.get(local_host)
    assert response.status_code == 200
    data = response.json()
    for elem in data:
        assert elem["type"]
        assert elem["is_categorical"]
        assert elem["id"]

def test_create_and_del_datatype():
    global test
    payload = json.dumps(test)
    response = requests.post(local_host,payload)
    assert response.status_code == 201
    data = response.json()
    response = requests.get(local_host + "/" + str(data["id"]))
    assert response.status_code == 200,print(response.json())
    response = requests.delete(local_host + "/" + str(data["id"]))
    assert response.status_code == 200
    response = requests.get(local_host + "/" + str(data["id"]))
    assert response.status_code == 404

