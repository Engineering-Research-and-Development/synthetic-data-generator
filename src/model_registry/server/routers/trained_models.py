
from fastapi import APIRouter,Path
from fastapi.params import Query
from starlette.responses import JSONResponse

from ..database.schema import TrainedModel, Features,TrainingInfo,ModelVersion,db,DataType
from ..database.handlers import trained_models as db_handler
from ..database.validation.schema import TrainedModel as PydanticTrainedModel, TrainedModelAndVersionIds, \
    TrainedModelAndVersions, \
    CreateTrainedModel, CreateModelVersion, CreateFeatures, CreateTrainingInfo,TrainedModelAndFeatureSchema

from peewee import DoesNotExist, IntegrityError,fn


router = APIRouter(prefix="/trained_models", tags=['Trained Models'])

@router.get("/",
            status_code=200,
            summary = "Get all the trained model in the repository",
            name = "Get all trained models",
            response_model=list[PydanticTrainedModel] | list[TrainedModelAndVersionIds])
async def get_all_trained_models(include_version_ids: bool | None = Query(description="Include a list of version ids"
                                " for each trained model",default=False)):
    """
    ## Get All Algorithms and Trained Models

    ### Endpoint
    **GET** `/`

    ### Name
    **Get all algorithms and trained models in the registry**

    ### Summary
    Retrieves all algorithms and trained models present in the repository. Optionally, it can include a list of version IDs for each trained model.

    ### Query Parameter
    | Name               | Type    | Description                                      | Default |
    |-------------------|--------|--------------------------------------------------|---------|
    | include_version_ids | `bool` | If `true`, includes a list of version IDs for each trained model | `false` |

    ### Response
    - **200 OK**: Returns a dictionary containing all algorithms and trained models.
      - If `include_version_ids = false`, the response contains detailed trained model information.
      - If `include_version_ids = true`, the response contains trained models with a list of associated version IDs.

    #### Response Body (Success)
    **Without `include_version_ids` (Default)**
    ```json
    {
      "algorithms": [
        {
          "id": 1,
          "name": "AlgorithmA",
          "description": "A sample algorithm"
        },
        {
          "id": 2,
          "name": "AlgorithmB",
          "description": "Another sample algorithm"
        }
      ],
      "trained_models": [
        {
          "id": 1,
          "name": "ModelA",
          "description": "A sample trained model",
          "created_at": "2024-01-01T12:00:00Z"
        },
        {
          "id": 2,
          "name": "ModelB",
          "description": "Another trained model",
          "created_at": "2024-02-10T15:30:00Z"
        }
      ]
    }
    **With `include_version_ids:**
        {
      "algorithms": [
        {
          "id": 1,
          "name": "AlgorithmA",
          "description": "A sample algorithm"
        },
        {
          "id": 2,
          "name": "AlgorithmB",
          "description": "Another sample algorithm"
        }
      ],
      "trained_models": [
        {
          "id": 1,
          "name": "ModelA",
          "version_ids": [101, 102, 103]
        },
        {
          "id": 2,
          "name": "ModelB",
          "version_ids": [201, 202]
        }
      ]
    }


    """
    if not include_version_ids:
        results = [PydanticTrainedModel(**trained_models) for trained_models in TrainedModel.select().dicts()]
        return results
    else: return db_handler.get_models_and_version_ids()


@router.get("/{trained_model_id}",
            status_code=200,
            name="Get a single trained model",
            summary="It returns a trained model given the id",
            responses={404: {"model": str}},
            response_model=TrainedModelAndFeatureSchema | TrainedModelAndVersions)
async def get_trained_model_id(trained_model_id: int = Path(description="The id of the trained model you want to get",examples=1)
                               ,include_versions: bool | None = Query(description="If the client wants all the versions "
                                                                                  "associated with the trained model",default=False),
                               version_id: int | None = Query(description="If the client wants to retrieve a specific "
                                                                                 "version", default=None)
                               ):
    """
    ## Get a Single Trained Model

    ### Endpoint
    **GET** `/{trained_model_id}`

    ### Name
    **Get a single trained model**

    ### Summary
    Retrieves a trained model by its ID. Optionally includes associated versions or feature schema.

    ### Path Parameter
    | Name               | Type  | Description                                               | Example |
    |-------------------|-------|-----------------------------------------------------------|---------|
    | trained_model_id  | `int` | The ID of the trained model to retrieve                   | `1`     |

    ### Query Parameters
    | Name           | Type    | Description                                                 | Default |
    |----------------|---------|-------------------------------------------------------------|---------|
    | include_versions | `bool` | If `true`, includes all versions associated with the trained model | `false` |
    | version_id     | `int`   | If provided, retrieves a specific version of the trained model | `None`  |

    ### Response
    - **200 OK**: Returns the requested trained model along with its associated versions or feature schema.
    - **404 Not Found**: If the trained model with the specified ID does not exist.

    #### Response Body (Success - Without Versions)
    ```json
    {
      "id": 1,
      "name": "TrainedModelA",
      "description": "A sample trained model",
      "feature_schema": [
        {
          "feature_name": "feature1",
          "feature_position": 1,
          "is_categorical": true,
          "datatype": "string"
        },
        {
          "feature_name": "feature2",
          "feature_position": 2,
          "is_categorical": false,
          "datatype": "integer"
        }
      ]
    }

    """
    if not include_versions:
        try:
            # Fetching the feature schema
            trained_model = (TrainedModel.select(
                TrainedModel,fn.JSON_AGG(
                    fn.JSON_BUILD_OBJECT('feature_name',Features.feature_name,'feature_position',Features.feature_position
                                         ,'is_categorical',DataType.is_categorical,'datatype',DataType.type))
            .alias("feature_schema"))
                     .join(Features)
                     .join(DataType)
                     .where(TrainedModel.id == trained_model_id)
                     .group_by(TrainedModel.id)).dicts().get()
        except DoesNotExist:
            return JSONResponse(status_code=404, content={"message": "No trained model has been found with this id"})
        return TrainedModelAndFeatureSchema(**trained_model)
    else:
        try:
            return db_handler.get_trained_model_versions(trained_model_id,version_id)
        except DoesNotExist:
            return JSONResponse(status_code=404, content={"message": "Trained Model not found"})



@router.post("/",
            name="Create a new training model",
            summary="It creates a trained model given the all the information,version,training infos and feature schema",
            responses={500: {"model": str}, 400: {"model":str},201:{"model":str}})
async def create_model_and_version(trained_model: CreateTrainedModel,
                                   version: CreateModelVersion,
                                   training_info: CreateTrainingInfo,
                                   feature_schema: list[CreateFeatures]):
    """
    ## Create a New Trained Model

    ### Endpoint
    **POST** `/`

    ### Name
    **Create a new training model**

    ### Summary
    Creates a new trained model given all the required information, including the model details, version, training information, and feature schema.

    ### Request Body
    The request should include the following details:

    - **trained_model**: Information about the new trained model (e.g., name, description).
    - **version**: Information about the model version.
    - **training_info**: Details regarding the training process.
    - **feature_schema**: A list of features associated with the model, each including a feature name, position, and datatype.

    #### Example Request Body
    ```json
    {
      "trained_model": {
        "name": "ModelA",
        "description": "A sample trained model"
      },
      "version": {
        "version": "1.0",
        "release_date": "2024-01-01"
      },
      "training_info": {
        "algorithm_id": 1,
        "training_date": "2024-01-01",
        "performance_metrics": {"accuracy": 0.95}
      },
      "feature_schema": [
        {
          "feature_name": "feature1",
          "feature_position": 1,
          "datatype": "float",
          "is_categorical": false
        },
        {
          "feature_name": "feature2",
          "feature_position": 2,
          "datatype": "string",
          "is_categorical": true
        }
      ]
    }

    """
    with db.atomic() as transaction:
         try:
               saved_tr = TrainedModel.create(**trained_model.model_dump())
         except IntegrityError:
             return JSONResponse(status_code=400, content={'message':"No algorithm has been found with this id"})
         # We need to check if the datatypes passed are allowed, i.e. present in the registry
         for feature in feature_schema:
             try:
                datatype =  DataType.select().where(DataType.type == feature.datatype)\
                .where(DataType.is_categorical == feature.is_categorical).get()
             except DoesNotExist:
                 transaction.rollback()
                 return JSONResponse(status_code=400, content={'message': "The datatype is currently not supported"
                                                                          ", to use it add it with POST /datatype"})
             try:
                 Features.insert(feature_name=feature.feature_name,feature_position=feature.feature_position
                                 ,datatype=datatype.id,trained_model=saved_tr.id).execute()
             except IntegrityError:
                 transaction.rollback()
                 return JSONResponse(status_code=500, content={'message': "Error in processing the request"})

         try:
             save_training_info = TrainingInfo.create(**training_info.model_dump())
         except IntegrityError:
             transaction.rollback()
             return JSONResponse(status_code=500, content={'message': "Error in processing the request"})

         try:
             ModelVersion.insert(**version.model_dump(),training_info = save_training_info.id
                                                     ,trained_model = saved_tr.id).execute()
         except IntegrityError:
             transaction.rollback()
             return JSONResponse(status_code=500, content={'message': "Error in processing the request"})

    return JSONResponse(status_code=201,content={"message": "Successfully saved model with the following id", "id": saved_tr.id})


@router.delete("/{trained_model_id}",
               status_code=200,
               name = "Deletes a trained model",
               summary = "Given an id it deletes only a specific version from the trained model leaving the model intact",
               responses = {404: {"model": str}}
                )
async def delete_train_model(trained_model_id: int,
                             version_id: int | None = Query(description="The id of the version to delete",default=None)):
    """
    ## Delete a Trained Model

    ### Endpoint
    **DELETE** `/{trained_model_id}`

    ### Name
    **Deletes a trained model**

    ### Summary
    Deletes a specific version from a trained model given its ID. The model itself remains intact.

    ### Path Parameter
    | Name               | Type  | Description                                               | Example |
    |-------------------|-------|-----------------------------------------------------------|---------|
    | trained_model_id  | `int` | The ID of the trained model to delete                     | `1`     |

    ### Query Parameter
    | Name           | Type    | Description                                                 | Default |
    |----------------|---------|-------------------------------------------------------------|---------|
    | version_id     | `int`   | The ID of the version to delete. If not specified, deletes all versions of the trained model. | `None`  |

    ### Response
    - **200 OK**: Successfully deleted the version or all versions associated with the trained model.
    - **404 Not Found**: If the trained model or version does not exist.

    #### Response Body (Success)
    ```json
    {
      "message": "Successfully deleted the trained model version(s)."
    }

    """
    try:
        model = TrainedModel.get_by_id(trained_model_id)
    except DoesNotExist:
        return JSONResponse(status_code=404, content={'message': "Model not present"})

    if version_id is None:
        query = (
            ModelVersion.select(ModelVersion.id.alias("version_id"),
                                TrainingInfo.id.alias("training_id"))
                .join(TrainingInfo).where(ModelVersion.trained_model == trained_model_id)
        )
    else:
        query = (
            ModelVersion.select(ModelVersion.id.alias("version_id"),
                                TrainingInfo.id.alias("training_id"))
            .join(TrainingInfo)
            .where(ModelVersion.trained_model == trained_model_id)
            .where(ModelVersion.id == version_id)
        )
        # This is the only case we need to return due to the fact that the client is trying to delete a specific version
        # Even if no version is found above, there is no anomalous behaviour. Since the for loop will not be executed
        # and only the model will be deleted
        if len(query.dicts()) == 0:
            return JSONResponse(status_code=404, content={'message': "This version has not been found!"})

    for row in query.dicts():
        ModelVersion.delete().where(ModelVersion.id == row["version_id"]).execute()
        TrainingInfo.delete().where(TrainingInfo.id == row["training_id"]).execute()

    if version_id is None:
        Features.delete().where(Features.trained_model == trained_model_id).execute()
        model.delete_instance()
