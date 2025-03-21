import os
import tempfile
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from ai_lib.job import job
from server.file_utils import create_trained_model_folder, cleanup_temp_dir
from server.couch_handlers import create_couch_entry, add_couch_data
from server.file_utils import create_server_repo_folder_structure
from server.middleware_handlers import (
    model_to_middleware,
    server_startup,
    generator_algorithms,
)
from server.validation_schema import InferRequestData, TrainRequest, CouchEntry

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))


@asynccontextmanager
async def lifespan(app: FastAPI):
    server_startup(APP_FOLDER)
    create_server_repo_folder_structure()
    # if is_couch_online():
    #     check_couch_model_registry()
    # else:
    #     raise ConnectionError("Could not reach couch db for server init. Is couch db online?")
    yield


generator = FastAPI(lifespan=lifespan)


def trim_name(elem: str):
    first_occ = elem.rfind(".")
    return elem[first_occ + 1 :]


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
    flag = False
    for algo in generator_algorithms:
        if algo["name"] == request["model"]["algorithm_name"]:
            flag = True
    if not flag:
        return JSONResponse(
            status_code=404,
            content="This algorithm is not implemented by the generator!",
        )
    # Here we calculate the unique name of the folder
    folder_id = (
        request["model"]["model_name"]
        + trim_name(request["model"]["algorithm_name"])
        + datetime.now().strftime("%Y%m%d.%H%M%S")
    )
    folder_path = Path(
        os.path.join(APP_FOLDER, Path(f"saved_models/trained_models/{folder_id}"))
    )
    # Here we create a temp directory
    with tempfile.TemporaryDirectory(
        dir=os.path.dirname(os.path.abspath(__file__))
    ) as tmp_dir:
        try:
            results, metrics, model, data = job(
                model_info=request["model"],
                dataset=request["dataset"],
                n_rows=request["n_rows"],
                save_filepath=tmp_dir,
                train=True,
            )
        except Exception as e:
            cleanup_temp_dir(tmp_dir)
            return JSONResponse(
                status_code=500, content=str(e)
            )
        create_trained_model_folder(folder_path, tmp_dir)
    dataset_name = "A name passed"
    # We invoke the model registry saving the model
    model_id = model_to_middleware(model, data, dataset_name, folder_path.as_posix())
    couch_doc = create_couch_entry()
    add_couch_data(
        couch_doc,
        new_data={
            "results": results,
            "metrics": metrics,
            "data": data.parse_tabular_data_json(),
        },
    )
    return CouchEntry(doc_id=couch_doc,model_path = folder_path.as_posix())


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
    if not os.path.isdir(Path(request["model"]["image"])):
        return JSONResponse(status_code=404, content="This model has not been found!")
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
    return CouchEntry(doc_id=couch_doc,model_path=request["model"]["image"])


@generator.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(generator, host="0.0.0.0", port=8010)
