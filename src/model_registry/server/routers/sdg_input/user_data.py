import os
from fastapi import APIRouter
from starlette.responses import JSONResponse

from .handlers import check_function_parameters, check_user_file, check_ai_model,check_features_created_types
from .schema import UserDataInput, GeneratorDataOutput

router = APIRouter(prefix="/sdg_input", tags=['SDG Input'])

generator_url = os.environ.get("generator_url", "http://localhost:8010")

@router.post("/",
             name="Synthetic Data Generator input collection",
             responses={400: {"model": str},
                        500: {"model": str}}
             )
async def collect_user_input(input_data: UserDataInput):
    """
    """
    data = input_data.model_dump()

    functions_id = check_function_parameters(data['functions'])
    if not functions_id:
        return JSONResponse(status_code=400, content="Error analysing functions")

    model = check_ai_model(data.get('ai_model'))
    if not model:
        return JSONResponse(status_code=400, content="Wrong model")

    body={}
    if data.get('user_file') is not None:
        user_file = check_user_file(data.get('user_file'))
        if not user_file:
            return JSONResponse(status_code=400, content="Error parsing input dataset")
        body=GeneratorDataOutput(
                            functions_id=functions_id,
                            n_rows=data.get('additional_rows'),
                            model=model,
                            dataset=user_file,
                            )


    if data.get('features_created') is not None:
        result,error = check_features_created_types(data.get('features_created'), functions_id)
        if not result:
            return JSONResponse(status_code=400, content="The functions chosen are not compatible with the following"
                                                         f' feature that you want to create ({error})')
        else:
            body = GeneratorDataOutput(
                functions_id=functions_id,
                n_rows=data.get('additional_rows'),
                model=model
            )

    if data.get('ai_model').get('new_model') and data.get('user_file'):
        url=generator_url+"/train"
    else:
        url=generator_url+"/infer"

    return JSONResponse(status_code=200, content="Invoking training/infer endpoint")


