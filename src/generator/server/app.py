from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from ai_lib.job import job
from server.couch_handlers import create_couch_entry, add_couch_data
from server.middleware_handlers import server_startup
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
    # TODO: Get save_filepath
    results, metrics, model, data = job(model_info=request["model"],
                                        dataset=request["dataset"],
                                        n_rows=request["n_rows"],
                                        save_filepath=".",
                                        train=True)
    add_couch_data(doc_id=couch_doc, new_data={"results": results,
                                                 "metrics": metrics,
                                                 "data": data})
    # TODO: Sync middleware with new model
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
    # TODO: Calculate file path
    results, metrics, model, data = job(model_info=request["model"],
                                        dataset=request["dataset"],
                                        n_rows=request["n_rows"],
                                        save_filepath=".",
                                        train=False)
    add_couch_data(doc_id=couch_doc, new_data={"results": results,
                                                 "metrics": metrics})

    return JSONResponse(status_code=200,content=CouchEntry(doc_id=couch_doc))



@generator.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(generator, host="0.0.0.0", port=8010)