from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks
from starlette.responses import RedirectResponse

from server.couch_handlers import create_couch_entry
from server.handlers import execute_train, execute_infer
from server.middleware_handlers import (
    server_startup,
)
from server.validation_schema import InferRequest, TrainRequest, CouchEntry


@asynccontextmanager
async def lifespan(app: FastAPI):
    server_startup()
    yield


generator = FastAPI(lifespan=lifespan)


@generator.post(
    "/train",
    responses={400: {"model": str}, 500: {"model": str}},
    response_model=CouchEntry,
)
async def train(request: TrainRequest, background_tasks: BackgroundTasks):
    """
    :param background_tasks: task to execute in background
    :param request: a request for train and infer
    :return:
    """
    couch_doc = create_couch_entry()
    background_tasks.add_task(execute_train, request, couch_doc)
    return CouchEntry(doc_id=couch_doc)


@generator.post(
    "/infer",
    responses={400: {"model": str}, 500: {"model": str}},
    response_model=CouchEntry,
)
async def infer_data(request: InferRequest, background_tasks):
    """
    :param background_tasks: task to execute in background
    :param request: a request for train and infer
    :return:
    """
    couch_doc = create_couch_entry()
    background_tasks.add_task(execute_infer, request, couch_doc)
    return CouchEntry(doc_id=couch_doc)


@generator.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(generator, host="0.0.0.0", port=8010)
