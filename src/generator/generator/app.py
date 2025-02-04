import importlib
import pkgutil
from typing import Union

from starlette.responses import RedirectResponse
from yaml import safe_load
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from exceptions.DataException import DataException
from exceptions.InputException import InputException
from exceptions.ModelException import ModelException
from generator.generate.infer import run_infer_job
from generator.generate.train import run_train_inference_job
from services.model_services import save_trained_model, save_system_model, delete_sys_model_by_id
from utils.parsing import parse_model_to_registry
from generator.input_schema import TrainRequest, InferRequestData, InferRequestNoData
from generator.output_schema import Response


def elaborate_request(body: dict) -> tuple[dict, list, list, int]:
    """

    :param body: a request body to be parsed
    :return:
    """
    model = body.get("model", {})
    behaviour_ids = body.get("functions_id", [])
    dataset = body.get("dataset", [])
    n_rows = body.get("n_rows", 100)

    if model == {}:
        raise ModelException("Model ID not found")

    # TODO: Implement Behaviours
    behaviours = []

    if n_rows < 1:
        raise InputException("Cannot Request less than 1 row!")

    return model, behaviours, dataset, n_rows


@asynccontextmanager
async def lifespan(app: FastAPI):

    config_file = pkgutil.get_data("generator", "config.yaml")
    config = safe_load(config_file)

    id_list = []

    print(config)
    list_models = []
    for pkg in config["system_models"]:
        root = pkg["root_lib"]
        for model in pkg["models"]:
            list_models.append(root+model)

    for model in list_models:
        module_name, class_name = model.rsplit('.', 1)
        module = importlib.import_module(module_name)
        Class = getattr(module, class_name)
        try:
            # TODO: refine with correct APIs
            response = save_system_model(Class.self_describe())
            id_list.append(response["id"])
        except ModelException as e:
            print(e)
            for mod_id in id_list:
                delete_sys_model_by_id(mod_id)
            #exit(-1)
    yield


generator = FastAPI(lifespan=lifespan)

@generator.post("/train",
                responses={400: {"model":str}, 500: {"model": str}},
                response_model=Response)
def train(request: TrainRequest):
    """
    :param request: a request for train and infer
    :return:
    """
    try:
        model_dict, behaviours, dataset, n_rows = elaborate_request(request.model_dump())
        results, metrics, model, data = run_train_inference_job(model_dict, behaviours, dataset, n_rows)
        try:
            model_to_save = parse_model_to_registry(model, data)
            save_trained_model(model_to_save)
        except ModelException as e:
            model.rollback_latest_version()
            raise ModelException(e)

        return JSONResponse(status_code=200,content={"result_data":results, "metrics": metrics})
    except InputException as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except ModelException as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except DataException as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": "An error occurred while processing the output"})




def infer(request: dict):
    try:
        results, metrics = run_infer_job(*elaborate_request(request))
        return JSONResponse(status_code=200,content={"result_data":results, "metrics": metrics})
    except InputException as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except ModelException as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except DataException as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": "An error occurred while processing the output"})


@generator.post("/infer",
                responses={400: {"model":str}, 500: {"model": str}},
                response_model=Response)
def infer_data(request: InferRequestData):
    """
    :param request: a request for train and infer
    :return:
    """
    return infer(request.model_dump())



@generator.post("/infer_nodata",
                responses={400: {"model":str}, 500: {"model": str}},
                response_model=Response)
def infer_nodata(request: InferRequestNoData):
    """
    :param request: a request for train and infer
    :return:
    """
    return infer(request.model_dump())


@generator.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(generator, host="0.0.0.0", port=8010)