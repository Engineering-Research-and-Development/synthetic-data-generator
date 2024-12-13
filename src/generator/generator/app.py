from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from exceptions.ModelException import ModelException
from generate.train import run_train_inference_job
from services.model_services import get_model_by_id

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

    if len(dataset) == 0:
        raise ValueError("Request data missing")

    if n_rows < 1:
        raise ValueError("Cannot Request less than 1 row!")

    return model, behaviours, dataset, n_rows



@generator.post("/train")
def train(request: dict):
    """

    :param request: a request for train and infer
    :return:
    """
    try:
        results, metrics = run_train_inference_job(*elaborate_request(request))
        print(results)
        print(metrics)
        return JSONResponse(status_code=200,content={"result_data":results, "metrics": metrics})
    except Exception as e:
        print("Out:", e)
        return JSONResponse(status_code=400, content={"message": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(generator, host="0.0.0.0", port=8010)