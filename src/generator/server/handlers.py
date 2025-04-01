from starlette.responses import JSONResponse

from ai_lib.job import job
from server.couch_handlers import add_couch_data
from server.file_utils import (
    check_latest_version,
    create_folder,
    delete_folder,
    save_model_payload,
    check_folder,
)
from server.middleware_handlers import generator_algorithm_names, model_to_middleware
from server.utilities import trim_name
from server.validation_schema import TrainRequest, InferRequest


def execute_train(request: TrainRequest, couch_doc: str):
    request = request.model_dump()
    # Check if the algorithm is implemented by the generator
    if request["model"]["algorithm_name"] not in generator_algorithm_names:
        return JSONResponse(
            status_code=500,
            content="This algorithm is not implemented by the generator!",
        )

    # Here we calculate the unique name of the folder
    model_folder_name = f"{request['model']['model_name']}-{trim_name(request['model']['algorithm_name'])}"
    new_version_name = f"v{check_latest_version(model_folder_name) + 1}"
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

    add_couch_data(
        couch_doc,
        new_data={
            "results": results,
            "metrics": metrics,
            "data": data.parse_tabular_data_json(),
        },
    )


def execute_infer(request: InferRequest, couch_doc: str):
    request = request.model_dump()
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
