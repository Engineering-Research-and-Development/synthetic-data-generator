from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from ai_lib.job import job
from server.couch_handlers import create_couch_entry, add_couch_data
from server.middleware_handlers import (save_new_trained_model, get_algorithm_path,
                                        create_feature_schema, fetch_model_save_path)
from server.validation_schema import InferRequestData, TrainRequest, CouchEntry


@asynccontextmanager
async def lifespan(app: FastAPI):
    # server_startup()

    yield



generator = FastAPI(lifespan=lifespan)

@generator.post("/train",
                responses={400: {"model":str}, 500: {"model": str}},
                response_model=CouchEntry)
async def train(request: TrainRequest):
    """
    :param request: a request for train and infer
    :return:
    """

    request = request.model_dump()
    couch_doc = create_couch_entry()
    # Check if the algorithm is implemented by the generator
    algorithm_path = get_algorithm_path(request["model"])
    if not algorithm_path:
        return JSONResponse(status_code=404,content="This algorithm is currently not implemented by the generator!")

    results, metrics, model, data = job(model_info=request["model"],
                                        dataset=request["dataset"],
                                        n_rows=request["n_rows"],
                                        save_filepath=algorithm_path,
                                        train=True)
    add_couch_data(doc_id=couch_doc, new_data={"results": results,
                                                 "metrics": metrics,
                                                 "data": data})
    # From the path we get the algorithm id
    algo_id = int(algorithm_path[algorithm_path.rfind('\\') + 1:])
    # From the dataset we create the current feature schema passed
    create_feature_schema(request["dataset"])
    # After the algorithm has been trained, a new trained model is created and hence we need to save it
    # in the local repository and be committed
    save_new_trained_model(model,algo_id,'trained_model/')
    return JSONResponse(status_code=200,content=CouchEntry(doc_id=couch_doc))




@generator.post("/infer",
                responses={400: {"model":str}, 500: {"model": str}},
                response_model=CouchEntry)
async def infer_data(request: InferRequestData):
    """
    :param request: a request for train and infer
    :return:
    """
    request = request.model_dump()
    couch_doc = create_couch_entry()
    # In this case we need to understand what training model is being called
    save_path = fetch_model_save_path(request["model"])
    results, metrics, model, data = job(model_info=request["model"],
                                        dataset=request["dataset"],
                                        n_rows=request["n_rows"],
                                        save_filepath= save_path,
                                        train=False)
    add_couch_data(doc_id=couch_doc, new_data={"results": results,
                                                 "metrics": metrics})
    # Since the model has been only used (no training/fine-tuning) no further saving is required
    return JSONResponse(status_code=200,content=CouchEntry(doc_id=couch_doc))



@generator.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(generator, host="0.0.0.0", port=8010)