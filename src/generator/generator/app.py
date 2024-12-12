from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from generate import train
from services.model_services import get_model_by_id

generator = FastAPI()

def elaborate_request(request: dict) -> tuple[dict, list, list]:
    """

    :param request: a request to be parsed
    :return:
    """
    model_id = request.get("model_id", -1)
    behaviour_ids = request.get("behaviour_ids", [])
    data = request.get("dataset", [])

    if model_id > 0:
        model = get_model_by_id(model_id)
    else:
        raise ValueError("Model ID not found")

    # TODO: Implement Behaviours
    behaviours = []

    if len(data) == 0:
        raise ValueError("Request data missing")

    return model, behaviours, data



@generator.post("/train")
def train(request: dict):
    """

    :param request: a request for train and infer
    :return:
    """
    try:
        model, behaviours, data = elaborate_request(request)
    except ValueError as e:
        print("Out:", e)
        return JSONResponse(status_code=400, content={"message": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(generator, host="0.0.0.0", port=8010)