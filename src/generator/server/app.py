from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from ai_lib.job import job
from server.couch_handlers import create_couch_entry, add_couch_data, init_db
from server.file_utils import (
    create_folder,
    delete_folder,
    check_folder,
    save_model_payload,
    check_latest_version,
)
from server.middleware_handlers import (
    model_to_middleware,
    generator_algorithm_names,
    server_startup,
)
from server.utilities import trim_name
from server.validation_schema import InferRequestData, TrainRequest, CouchEntry


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    server_startup()
    yield


generator = FastAPI(lifespan=lifespan)


@generator.post(
    "/train",
    responses={400: {"model": str}, 500: {"model": str}},
    response_model=CouchEntry,
)
async def train(request: TrainRequest):
    """
    :param request: a request for train and infer
    :return:
    """
    request = request.model_dump()
    # Check if the algorithm is implemented by the generator
    if request["model"]["algorithm_name"] not in generator_algorithm_names:
        return JSONResponse(
            status_code=500,
            content="This algorithm is not implemented by the generator!",
        )

    # Here we calculate the unique name of the folder
    model_folder_name = f"{request["model"]["model_name"]}-{trim_name(request["model"]["algorithm_name"])}"
    new_version_name = f"v{check_latest_version(model_folder_name)+1}"
    folder_id = f"{model_folder_name}-{new_version_name}"

    folder_path = create_folder(folder_id)
    try:
        results, metrics, model, data = job(
            model_info=request["model"],
            dataset=request["dataset"],
            n_rows=request["n_rows"],
            save_filepath=folder_path,
            train=True,
        )
    except (ValueError, TypeError) as e:
        delete_folder(folder_path)
        return JSONResponse(status_code=500, content=str(e))

    # We invoke the model registry saving the model, if failing delete trained model
    try:
        model_payload = model_to_middleware(
            model, data, "dataset_name", str(folder_path), new_version_name
        )
        save_model_payload(folder_path, model_payload)
    except KeyError:
        delete_folder(folder_path)
        return JSONResponse(
            status_code=500,
            content=str("Impossible to link algorithms to trained model"),
        )

    couch_doc = create_couch_entry()
    add_couch_data(
        couch_doc,
        new_data={
            "results": results,
            "metrics": metrics,
            "data": data.parse_tabular_data_json(),
        },
    )
    return CouchEntry(doc_id=couch_doc)


@generator.post(
    "/infer",
    responses={400: {"model": str}, 500: {"model": str}},
    response_model=CouchEntry,
)
async def infer_data(request: InferRequestData):
    """
    :param request: a request for train and infer
    :return:
    """
    request = request.model_dump()
    couch_doc = create_couch_entry()
    if not check_folder(request["model"]["image"]):
        return JSONResponse(status_code=500, content="This model has not been found!")
    # In this case since train is false the model will be loaded
    results, metrics, model, data = job(
        model_info=request["model"],
        dataset=request["dataset"],
        n_rows=request["n_rows"],
        save_filepath="",
        train=False,
    )

    add_couch_data(doc_id=couch_doc, new_data={"results": results, "metrics": metrics})
    # Since the model has been only used (no training/fine-tuning) no further saving is required
    return CouchEntry(doc_id=couch_doc)


@generator.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(generator, host="0.0.0.0", port=8010)
