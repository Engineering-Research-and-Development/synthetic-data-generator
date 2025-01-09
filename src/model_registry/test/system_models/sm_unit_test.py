import json
import requests

test = {
  "system_model":
  {
    "name": "Test_System_Model3",
    "description": "A default description",
    "loss_function": "A loss function"
  },
  "data_types": [
      {
          "type":"string",
          "is_categorical":"true"
      },
      {
          "type":"string",
          "is_categorical":"true"
      }

  ]

}
localhost = "http://127.0.0.1:8000/system_models"

def test_create_system_model():
    global test
    model = json.dumps(test)
    response = requests.post(localhost,model)
    assert response.status_code == 201, print(response.json())
    data = response.json()
    # We now check that the system model has been created
    response = requests.get(localhost + "/" + str(data["name"]))
    assert response.status_code == 200, print(response.json())
    data = response.json()
    assert data["name"] == test["system_model"]["name"]
    assert data["description"] == test["system_model"]["description"]
    assert data["loss_function"] == test["system_model"]["loss_function"]
    for datatype,categorical,test_datatype in zip(data["allowed_datatype"],data["is_categorical"],test["data_types"]):
        assert datatype == test_datatype["type"]
        assert categorical == bool(test_datatype["is_categorical"])


def test_get_all_system_models(get_all_system_models):
    response = requests.get(localhost)
    assert response.status_code == 200
    data = response.json()
    for model,test_model in zip(data,get_all_system_models):
        assert model["name"] ==  test_model["name"]
        assert model["description"] == test_model["description"]
        assert model["loss_function"] ==  test_model["loss_function"]
        assert model["allowed_datatype"] == test_model["allowed_datatype"]
        assert model["is_categorical"] == test_model["is_categorical"]


def test_get_system_models_by_name(get_all_system_models):
    for test_model in get_all_system_models:
        response = requests.get(localhost + "/" + test_model["name"])
        assert response.status_code == 200
        model = response.json()
        assert model["name"] == test_model["name"]
        assert model["description"] == test_model["description"]
        assert model["loss_function"] == test_model["loss_function"]
        assert model["allowed_datatype"] == test_model["allowed_datatype"]
        assert model["is_categorical"] == test_model["is_categorical"]
    assert requests.get(localhost + "/1000").status_code == 404


def test_delete_system_models():
    global test
    assert requests.delete(localhost + "/" + test["system_model"]["name"]).status_code == 200
    assert requests.get(localhost + "/" + test["system_model"]["name"]).status_code == 404

