import pytest
from ai_lib.job import job
import json
import os


train_request = json.load(open("train_test.json"))
infer_request = json.load(open("infer_test.json"))
infer_nodata_request = json.load(open("infer_test_nodata.json"))

def setup():
    if not os.path.isdir("./outputs"):
        os.mkdir("./outputs")

def test_train():

    model_info = train_request["model"]
    dataset = train_request["dataset"]
    n_rows = train_request["n_rows"]
    save_filepath = "./outputs/"
    setup()

    results, metrics, model, data = job(model_info=model_info, dataset=dataset, n_rows=n_rows,
                                        save_filepath=save_filepath, train=True)
    assert type(results) == list
    assert results is not None
    assert metrics is not None
    assert model is not None
    assert data is not None


def test_infer():


    model_info = infer_request["model"]
    dataset = infer_request["dataset"]
    n_rows = infer_request["n_rows"]
    save_filepath = "./outputs/"
    setup()

    results, metrics, model, data = job(model_info=model_info, dataset=dataset, n_rows=n_rows,
                                        save_filepath=save_filepath, train=False)
    assert type(results) == list
    assert results is not None
    assert metrics is not None
    assert model is not None
    assert data is not None


def test_infer_nodata():

    model_info = infer_nodata_request["model"]
    n_rows = infer_nodata_request["n_rows"]
    save_filepath = "./outputs/"
    setup()

    results, metrics, model, data = job(model_info=model_info, dataset=[], n_rows=n_rows,
                                        save_filepath=save_filepath, train=False)
    assert type(results) == list
    assert results is not None
    assert metrics is not None
    assert model is not None
    assert data is not None
