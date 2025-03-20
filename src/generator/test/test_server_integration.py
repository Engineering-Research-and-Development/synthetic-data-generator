import os
import json
import requests
from pathlib import Path

generator_url = os.environ.get("GENERATOR_URL", "http://generator:8010/")


def test_generator_train():
    # Loading data for post
    with open(os.path.abspath(Path("ai_lib/test/train_test.json"))) as file:
        to_post = json.load(file)
    response = requests.post(f"{generator_url}train", json=to_post)
    assert response.status_code == 200, print(response.content)


def test_generator_infer():
    with open(os.path.abspath(Path("ai_lib/test/infer_test.json"))) as file:
        to_post = json.load(file)
    print(to_post)
    response = requests.post(f"{generator_url}infer", json=to_post)
    assert response.status_code == 200, print(response.content)
