from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from ai_lib.generator.generate.train import run_train_inference_job
from ai_lib.generator.generate.infer import run_infer_job
from ai_lib.utils.parsing import parse_model_to_registry

from server.middleware_handlers import save_trained_model
from server.validation_schema import InferRequestData, TrainRequest, GeneratedResponse


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


generator = FastAPI(lifespan=lifespan)

@generator.post("/train",
                responses={400: {"model":str}, 500: {"model": str}},
                response_model=GeneratedResponse)
def train(request: TrainRequest):
    """
    :param request: a request for train and infer
    :return:
    """
    try:
        request = request.model_dump()
        results, metrics, model, data = run_train_inference_job(request["model"], [], request["dataset"],
                                                                request["n_rows"])
        model_to_save = parse_model_to_registry(model, data)
        save_trained_model(model_to_save)

        return JSONResponse(status_code=200,content={"result_data":results, "metrics": metrics})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"error": "An error occurred while processing the output"})


@generator.post("/infer",
                responses={400: {"model":str}, 500: {"model": str}},
                response_model=GeneratedResponse)
def infer_data(request: InferRequestData):
    """
    :param request: a request for train and infer
    :return:
    """
    request = request.model_dump()
    results, metrics = run_infer_job(request["model"], [], request["dataset"], request["n_rows"])
    return JSONResponse(status_code=200,content={"result_data":results, "metrics": metrics})


@generator.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(generator, host="0.0.0.0", port=8010)