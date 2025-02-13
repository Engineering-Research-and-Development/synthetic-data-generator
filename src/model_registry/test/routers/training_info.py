import requests

from ..conftest import server,port


endpoint = "/training_info"

def test_get_training_info():
    response = requests.get(f"{server}:{port}{endpoint}" + "/1")
    assert response.status_code == 200
    data = response.json()
    assert data['loss_function']
    assert data['train_loss']
    assert data['val_loss']
    assert data['train_samples']
    assert data['val_samples']
    assert data['id']