from ai_lib.job import job
import json


train_request = json.load(open("train_test.json"))
infer_request = json.load(open("infer_test.json"))
infer_nodata_request = json.load(open("infer_test_nodata.json"))

def test_train():

    model_info = train_request["model"]
    dataset = train_request["dataset"]
    n_rows = train_request["n_rows"]
    save_filepath = "./outputs/"

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

    print(model_info)
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

    print(model_info)
    results, metrics, model, data = job(model_info=model_info, dataset=[], n_rows=n_rows,
                                        save_filepath=save_filepath, train=False)
    assert type(results) == list
    assert results is not None
    assert metrics is not None
    assert model is not None
    assert data is not None
