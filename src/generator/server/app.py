from contextlib import asynccontextmanager
import pickle
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse

from server.middleware_handlers import model_to_middleware, load_trees, server_sync_algorithms, \
    server_sync_trained, remote_sync
from server.validation_schema import InferRequestData, TrainRequest, GeneratedResponse

# from ai_lib.data_generator.generate.train import run_train_inference_job
# from ai_lib.data_generator.generate.infer import run_infer_job


@asynccontextmanager
async def lifespan(app: FastAPI):
   # Pre-work: we fetch the B+Trees for algorithms and trained models
   tree_algorithms,tree_trained_models = load_trees()
   # 1.  Analyse the existing folders, looking for trained_models models *
   mock_generator_trained_models = []
   server_sync_trained(tree_trained_models,mock_generator_trained_models)
   # 2. Synchronize (POST/DELETE) with the middleware for existing trained_models models
   remote_sync(tree_trained_models,'trained_models/?include_version_ids=False&index_by_id=True')
   # 3.  Analyse the existing folders, looking for algorithms
   # This is mock data at the moment
   mock_generator_algorithms = [{'name':'System_' + str(i), 'description': 'A description'
                       , 'default_loss_function':'A loss function','folder_path':'server/saved_models/algorithms/i'} for i in range(10)]
   # 3.a We sync with local algorithm that the generator has
   server_sync_algorithms(tree_algorithms,mock_generator_algorithms)
   # 4. Synchronize (POST/DELETE) with the middleware for existing algorithms
   remote_sync(tree_algorithms,'algorithms/?include_allowed_datatypes=False&indexed_by_names=True')

   yield



generator = FastAPI(lifespan=lifespan)

@generator.post("/train",
                responses={400: {"model":str}, 500: {"model": str}},
                response_model=GeneratedResponse)
def train(request: TrainRequest):
    """
    :param request: a request for train and infer
    :return:
    """
    #
    # request = request.model_dump()
    # results, metrics, model, data = run_train_inference_job(request["model"], [], request["dataset"],
    #                                                         request["n_rows"])
    # model_to_middleware(model, data)
    #
    # return JSONResponse(status_code=200,content={"result_data":results, "metrics": metrics})
    pass


@generator.post("/infer",
                responses={400: {"model":str}, 500: {"model": str}},
                response_model=GeneratedResponse)
def infer_data(request: InferRequestData):
    """
    :param request: a request for train and infer
    :return:
    """
    # request = request.model_dump()
    # results, metrics = run_infer_job(request["model"], [], request["dataset"], request["n_rows"])
    # return JSONResponse(status_code=200,content={"result_data":results, "metrics": metrics})
    pass


@generator.get("/", include_in_schema=False)
async def home_to_docs():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(generator, host="0.0.0.0", port=8010)