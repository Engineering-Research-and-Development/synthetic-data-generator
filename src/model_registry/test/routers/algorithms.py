from .conftest import server,port


endpoint =  "/algorithms"


test_algorithm = {
  "algorithm":
  {
    "name": "TestTest2",
    "description": "A default description",
    "default_loss_function": "A loss function"
  },
  "allowed_data": [
      {
          "datatype":"DataType_0",
          "is_categorical":"true"
      },
      {
          "datatype":"DataType_0",
          "is_categorical":"true"
      }

  ]

}


import random
from copy import deepcopy

def test_create_algorithm(client):
    local_algo = deepcopy(test_algorithm)
    local_algo['algorithm']['name'] = (local_algo['algorithm']['name'] + str(random.randint(0,100))
                                       + str(random.randint(0,100)))
    response = client.post(f"{server}:{port}{endpoint}",json=local_algo)
    assert response.status_code == 201,print(local_algo['algorithm']['name'],response.content)
    id = response.json()['id']
    response = client.get(f"{server}:{port}{endpoint}" + "/" + str(id))
    assert response.status_code == 200,print(response.content)

def test_create_bad_name_algorithm(client):
    local_algo = deepcopy(test_algorithm)
    local_algo['algorithm']['name'] = 'System_1'
    assert client.post(f"{server}:{port}{endpoint}",json=local_algo).status_code == 400

def test_create_bad_datatype_algorithm(client):
    local_algo = deepcopy(test_algorithm)
    local_algo['allowed_data'][0]['datatype'] = 'bad_datatype'
    assert client.post(f"{server}:{port}{endpoint}",json=local_algo).status_code == 400

def test_get_all(client):
    response = client.get(f"{server}:{port}{endpoint}")
    assert response.status_code == 200
    random_algo = random.choice(response.json())
    assert random_algo['id']
    assert random_algo['name']
    assert random_algo['description']
    assert random_algo['default_loss_function']

def test_get_all_datatypes(client):
    response = client.get(f"{server}:{port}{endpoint}" + "?include_allowed_datatypes=True")
    assert response.status_code == 200
    assert len(response.json()) > 0
    random_algo = random.choice(response.json())
    assert random_algo['id']
    assert random_algo['name']
    assert random_algo['description']
    assert random_algo['default_loss_function']
    if random_algo['allowed_data']:
        random_data = random.choice(random_algo['allowed_data'])
        assert random_data['datatype']
        assert random_data['is_categorical']


def test_get_algo_by_id(client):
    response = client.get(f"{server}:{port}{endpoint}" + "/2")
    assert response.status_code == 200,print(response.content)
    data = response.json()
    assert data['id']
    assert data['name']
    assert data['description']
    assert data['default_loss_function']

def test_get_bad_algo_by_id(client):
    response = client.get(f"{server}:{port}{endpoint}" + "/1000")
    assert response.status_code == 404

def test_get_algo_by_id_with_datatypes(client):
    response = client.get(f"{server}:{port}{endpoint}" + "/2/?include_allowed_datatypes=True")
    assert response.status_code == 200
    data = response.json()
    assert data['id']
    assert data['name']
    assert data['description']
    assert data['default_loss_function']
    assert data['allowed_data']

def test_get_bad_algo_by_id_with_datatypes(client):
    response = client.get(f"{server}:{port}{endpoint}" + "/1000/allowed_datatypes")
    assert response.status_code == 404


def test_delete_algo(client):
    local_algo = deepcopy(test_algorithm)
    local_algo['algorithm']['name'] = local_algo['algorithm']['name'] + str(random.randint(0,100))
    response = client.post(f"{server}:{port}{endpoint}",json=local_algo)
    assert response.status_code == 201
    created_id = response.json()['id']
    response = client.delete(f"{server}:{port}{endpoint}" + "/" + str(created_id))
    assert response.status_code == 200
    assert client.get(f"{server}:{port}{endpoint}" + "/" + str(created_id)).status_code == 404

def test_bad_delete(client):
    assert client.delete(f"{server}:{port}{endpoint}" + "/1000").status_code == 404
