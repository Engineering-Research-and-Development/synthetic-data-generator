from fastapi import APIRouter
from starlette.responses import JSONResponse

from routers.sdg_input.handlers import check_functions, check_selected_model, check_user_file, \
    check_selected_version, check_features_created
from routers.sdg_input.schema import UserDataInput

router = APIRouter(prefix="/sdg_input")

@router.post("/")
async def collect_user_input(input_data: UserDataInput):
    data = input_data.model_dump()

    if not check_functions(data['functions']):
        return JSONResponse(status_code=422, content="Error analysing functions")

    if not check_selected_model(input_data.selected_model):
        return JSONResponse(status_code=422, content="Wrong selected model")

    if not check_user_file(input_data.user_file):
        return JSONResponse(status_code=422, content="Error parsing input dataset")

    if not check_selected_version(input_data.selected_version):
        return JSONResponse(status_code=422, content="Wrong version")

    if not check_features_created(input_data.features_created):
        return JSONResponse(status_code=422, content="Error parsing features")

    return JSONResponse(status_code=200, content="Data augmentation started")


