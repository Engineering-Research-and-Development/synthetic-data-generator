import requests
from conftest import middleware,couch,generator

def check_connectivity(url):
    response = requests.get(url)
    assert response.status_code == 200

def test_middleware():
    check_connectivity(middleware)

def test_couch():
    check_connectivity(couch)

def test_generator():
    check_connectivity(generator)
