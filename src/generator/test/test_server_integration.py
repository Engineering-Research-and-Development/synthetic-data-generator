import os
import json
import requests
from pathlib import Path

generator_url = os.environ.get("GENERATOR_URL", "http://generator:8010/")
current_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.join(current_folder, "..")
train_test = os.path.join(root_folder, "ai_lib/test/train_test.json")
infer_test = os.path.join(root_folder, "ai_lib/test/infer_test.json")

"""
def test_generator_train():
    # Loading data for post
    with open(train_test) as file:
        to_post = json.load(file)
    response = requests.post(f"{generator_url}train", json=to_post)
    assert response.status_code == 200, print(response.content)


def test_generator_infer():
    with open(infer_test) as file:
        to_post = json.load(file)
    response = requests.post(f"{generator_url}infer", json=to_post)
    assert response.status_code == 200, print(response.content)
"""