from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from exceptions.DataException import DataException
from exceptions.InputException import InputException
from exceptions.ModelException import ModelException
from generate.infer import run_infer_job
from generate.train import run_train_inference_job
from services.model_services import save_trained_model
from utils.parsing import parse_model_to_registry

generator = FastAPI()

def elaborate_request(body: dict) -> tuple[dict, list, list, int]:
    """

    :param body: a request body to be parsed
    :return:
    """
    model = body.get("model", {})
    behaviour_ids = body.get("behaviour_ids", [])
    dataset = body.get("dataset", [])
    n_rows = body.get("n_rows", 100)

    if model == {}:
        raise ModelException("Model ID not found")

    # TODO: Implement Behaviours
    behaviours = []

    if n_rows < 1:
        raise InputException("Cannot Request less than 1 row!")

    return model, behaviours, dataset, n_rows



@generator.post("/train")
def train(request: dict):
    """
    :param request: a request for train and infer
    :return:
    """
    try:
        model_dict, behaviours, dataset, n_rows = elaborate_request(request)
        results, metrics, model = run_train_inference_job(model_dict, behaviours, dataset, n_rows)
        model_to_save = parse_model_to_registry(model, dataset)

        try:
            print(model_to_save)
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



@generator.post("/infer")
def train(request: dict):
    """
    :param request: a request for train and infer
    :return:
    """
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



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(generator, host="0.0.0.0", port=8010)