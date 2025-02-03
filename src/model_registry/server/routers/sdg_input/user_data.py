from fastapi import APIRouter
from starlette.responses import JSONResponse

from routers.sdg_input.handlers import check_functions, check_selected_model, check_user_file, \
    check_features_created, check_new_model
from routers.sdg_input.schema import UserDataInput

router = APIRouter(prefix="/sdg_input")

@router.post("/")
async def collect_user_input(input_data: UserDataInput):
    data = input_data.model_dump()

    if not check_functions(data['functions']):
        return JSONResponse(status_code=422, content="Error analysing functions")

    if data['new_model']:
        if not check_new_model(data['selected_model'], data["new_model_name"]):
            return JSONResponse(status_code=422, content="Wrong new model")
    else:
        if not check_selected_model(data['selected_model'], data["model_version"]):
            return JSONResponse(status_code=422, content="Wrong selected model")

    if not check_user_file(data['user_file']):
        return JSONResponse(status_code=422, content="Error parsing input dataset")

    if not check_features_created(data['features_created']):
        return JSONResponse(status_code=422, content="Error parsing features")

    return JSONResponse(status_code=200, content="Data augmentation started")


