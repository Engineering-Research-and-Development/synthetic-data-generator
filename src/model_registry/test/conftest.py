"""This module is needed to define a bunch of functions and data that are needed in order to carry out all the tests .
For more information about why this module is needed, check:
https://stackoverflow.com/questions/17801300/how-to-run-a-method-before-all-tests-in-all-classes"""
import pytest
import requests

def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """


@pytest.fixture
def train_models_test_data():
    return requests.get("http://127.0.0.1:8000/trained_models").json()


@pytest.fixture
def train_model_versions(train_models_test_data):
    """
    This function returns for each train model all his versions and feature schema
    :param train_models_test_data: A list of all train models in the db
    :return: For each train model it returns his versions and feature schema
    """
    payload = []
    for model in train_models_test_data:
        data = requests.get("http://127.0.0.1:8000/trained_models/"+ str(model["id"]) +"/versions").json()
        print(data)
        payload.append({"id":model["id"],"versions":data["versions"],"feature_schema":data["feature_schema"]})
    return payload


@pytest.fixture
def train_model_feature_schemas():
    return requests.get("http://127.0.0.1:8000/trained_models").json()
