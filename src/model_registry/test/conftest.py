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
