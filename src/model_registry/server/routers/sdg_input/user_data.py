import requests
from fastapi import APIRouter
from starlette.responses import JSONResponse

from routers.sdg_input.handlers import check_function_parameters, check_user_file, check_ai_model
from routers.sdg_input.schema import UserDataInput, GeneratorDataOutput

router = APIRouter(prefix="/sdg_input")

@router.post("/")
async def collect_user_input(input_data: UserDataInput):
    data = input_data.model_dump()

    function_ids = check_function_parameters(data['functions'])
    if not function_ids:
        return JSONResponse(status_code=422, content="Error analysing functions")

    model = check_ai_model(data.get('ai_model'))
    if not model:
        return JSONResponse(status_code=422, content="Wrong model")

    body={}
    if data.get('user_file') is not None:
        user_file = check_user_file(data.get('user_file'))
        if not user_file:
            return JSONResponse(status_code=422, content="Error parsing input dataset")

        body=GeneratorDataOutput(function_ids=function_ids,
                            n_rows=data.get('additional_rows'),
                            model=model,
                            dataset=user_file,
                            )

    if data.get('ai_model').get('new_model'):
        url="http://localhost:8010/train"
    else:
        url="http://localhost:8010/fine_tune"

    return JSONResponse(content=body.model_dump())
    request = requests.post(url, json=GeneratorDataOutput.model_json_schema())
    if request.status_code == 200:
        return JSONResponse(status_code=200, content="Data augmentation started")
    else:
        return JSONResponse(status_code=500, content="Generator error")


