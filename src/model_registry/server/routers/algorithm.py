from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from ..database.validation.schema import CreateAlgorithm,Algorithm as PydanticAlgorithm, CreateAllowedData\
    ,AlgorithmAndAllowedDatatypes
from ..database.schema import DataType, AllowedDataType, db, Algorithm, TrainedModel

from ..routers.trained_models import delete_train_model

from peewee import DoesNotExist,IntegrityError,fn,JOIN

router = APIRouter(prefix="/algorithms", tags=['Algorithms'])


@router.post("/",
             status_code=201,
             name="Create a new algorithm",
             summary="It creates an algorith  given the all the information and allowed datatypes",
             responses={500: {"model": str}, 400: {"model": str}, 201: {"model": str}}
             )
async def add_algorithm_and_datatype(algorithm: CreateAlgorithm, allowed_data: list[CreateAllowedData]):
    """
    ## `add_algorithm_and_datatype`

    ### Endpoint:
    `POST /`

    ### Description:
    This endpoint creates a new algorithm by saving its information and associating it with a list of allowed data types. It handles the algorithm creation and checks for uniqueness in algorithm names. Additionally, it validates the compatibility of the provided data types with the supported types.

    ### Request Body:
    - `algorithm` (Type: `CreateAlgorithm`): Contains the details of the algorithm to be created.
    - `allowed_data` (Type: `list[CreateAllowedData]`): A list of data types that are allowed to be associated with the algorithm. Each entry contains a `datatype` and a `is_categorical` flag.

    ### Response:
    - **201 Created**: If the algorithm and associated data types are successfully created, returns a message with the newly created algorithm’s ID.
      - **Example Response**:
        ```json
        {
          "message": "Created algorithm with id",
          "id": "algorithm_id"
        }
        ```

    - **400 Bad Request**: If the algorithm name is not unique, or if the provided data type is not supported.
      - **Example Response**:
        ```json
        {
          "message": "Algorithm names must be uniques! Try another name!"
        }
        ```
        or
        ```json
        {
          "message": "The datatype is currently not supported, to use it add it with POST /datatype"
        }
        ```

    - **500 Internal Server Error**: If there is an unexpected error when processing the request.
      - **Example Response**:
        ```json
        {
          "message": "Error in processing the request"
        }
        ```

    ### Success Response:
    - **Status Code**: `201`
    - **Content**: A JSON object containing a message and the ID of the created algorithm.

    ### Error Responses:
    - **Status Code**: `400`
      - **Content**: Error message regarding unique algorithm names or unsupported data types.

    - **Status Code**: `500`
      - **Content**: General error message when there is an issue during processing.

    ### Error Handling:
    - If the algorithm name already exists, a `400 Bad Request` error is returned.
    - If an unsupported data type is provided, the transaction is rolled back, and a `400 Bad Request` error is returned, suggesting the user add the data type via the `/datatype` endpoint.
    - If an internal server error occurs, the transaction is rolled back, and a `500 Internal Server Error` is returned.

    ### Database Transactions:
    - A transaction is used to ensure that if any part of the process fails (e.g., the insertion of a data type or algorithm), the entire operation is rolled back, maintaining data integrity.

    ### Example Flow:
    1. A POST request is sent with the algorithm details and a list of allowed data types.
    2. The algorithm is created if the name is unique.
    3. Each provided data type is validated.
    4. If the data type exists, it is associated with the newly created algorithm.
    5. If all steps are successful, a success message with the algorithm ID is returned.

    """
    with db.atomic() as transaction:
        try:
            saved_algo = Algorithm.create(**algorithm.model_dump())
        except IntegrityError:
            return JSONResponse(status_code=400, content={'message': "Algorithm names must be uniques! Try another name!"})
        for feature in allowed_data:
            try:
                datatype = DataType.select().where(DataType.type == feature.datatype) \
                    .where(DataType.is_categorical == feature.is_categorical).get()
            except DoesNotExist:
                transaction.rollback()
                return JSONResponse(status_code=400,content={"message":"The datatype is currently not supported"
                                                                              ", to use it add it with POST /datatype"})
            try:
                AllowedDataType.insert(datatype=datatype.id, algorithm_id=saved_algo.id).execute()
            except IntegrityError:
                transaction.rollback()
                return JSONResponse(status_code=500, content={'message': "Error in processing the request"})

    return {"message": "Created algorithm with id", "id": str(saved_algo.id)}

@router.get("/",
            status_code=200,
            name="Get all algorithms",
            description="It returns all the algorithms present in the model registry",
            response_model=list[PydanticAlgorithm] | list[AlgorithmAndAllowedDatatypes])
async def get_all_algorithms(include_allowed_datatypes: bool | None = Query(description="Include the allowed datatypes"
                              "for each algorithm present in the system",default=False)):

    """
    ## `get_all_algorithms`

    ### Endpoint:
    `GET /`

    ### Description:
    This endpoint retrieves all algorithms currently stored in the model registry. You can choose whether to include the allowed data types associated with each algorithm. By default, the response will only include basic algorithm details, but you can request more information about the data types each algorithm supports.

    ### Query Parameters:
    - `include_allowed_datatypes` (Type: `bool | None`):
      - Optional query parameter to determine whether to include the allowed data types for each algorithm.
      - **Default**: `False`
      - **Description**: If set to `True`, the response will include the allowed data types for each algorithm. If `False`, only basic algorithm information is returned.

    ### Response:
    - **200 OK**: Returns a list of algorithms, with or without allowed data types, depending on the `include_allowed_datatypes` parameter.

      If `include_allowed_datatypes=False` (default):
      - **Response Model**: A list of `PydanticAlgorithm` objects, each representing a basic algorithm.
        - **Example**:
          ```json
          [
            {
              "id": "algorithm_id",
              "name": "algorithm_name",
              "description": "algorithm_description"
            },
            ...
          ]
          ```

      If `include_allowed_datatypes=True`:
      - **Response Model**: A list of `AlgorithmAndAllowedDatatypes` objects, each representing an algorithm with its associated allowed data types.
        - **Example**:
          ```json
          [
            {
              "id": "algorithm_id",
              "name": "algorithm_name",
              "allowed_data": [
                {
                  "datatype": "datatype_name",
                  "is_categorical": true
                },
                ...
              ]
            },
            ...
          ]
          ```

    ### Error Handling:
    This endpoint is a read-only operation and doesn't require complex error handling. However, if any errors arise (e.g., database connection issues), a standard internal error (500) will be returned by the framework.

    ### Database Query:
    - If `include_allowed_datatypes=False`: The function selects basic details of all algorithms from the `Algorithm` table and returns them as a list of `PydanticAlgorithm` objects.
    - If `include_allowed_datatypes=True`: The function performs a more complex query, joining the `Algorithm`, `AllowedDataType`, and `DataType` tables to retrieve each algorithm’s allowed data types, returning the results as `AlgorithmAndAllowedDatatypes` objects.

    ### Example Flow:
    1. A GET request is made to retrieve all algorithms.
    2. If the `include_allowed_datatypes` parameter is set to `False` (or omitted), only the basic algorithm details are returned.
    3. If the `include_allowed_datatypes` parameter is set to `True`, each algorithm's allowed data types are also included in the response.
    4. The data is returned in a structured JSON format, either as a list of basic algorithms or as a list of algorithms with their allowed data types.

    ### Example Request:
    - `GET /?include_allowed_datatypes=true`

    ### Example Response (when `include_allowed_datatypes=True`):
    ```json
    [
      {
        "id": "algorithm_id",
        "name": "algorithm_name",
        "allowed_data": [
          {
            "datatype": "string",
            "is_categorical": true
          },
          {
            "datatype": "integer",
            "is_categorical": false
          }
        ]
      }
    ]
    """
    if not include_allowed_datatypes:
        results = [PydanticAlgorithm(**sys_model) for sys_model in Algorithm.select().dicts()]
        return results
    else:
        query = (Algorithm.select(
            Algorithm,
            fn.JSON_AGG(fn.JSON_BUILD_OBJECT('datatype', DataType.type, 'is_categorical', DataType.is_categorical))
            .alias("allowed_data"))
                 .join(AllowedDataType, JOIN.LEFT_OUTER)
                 .join(DataType, JOIN.LEFT_OUTER)
                 .group_by(Algorithm.id))
        return [AlgorithmAndAllowedDatatypes(**row) for row in query.dicts()]



@router.get("/{algorithm_id}",
            status_code=200,
            name="Get algorithm by id",
            summary="It returns an algorithm given the id",
            responses={404: {"model": str}},
            response_model=PydanticAlgorithm | AlgorithmAndAllowedDatatypes)
async def get_algorithm_by_id(algorithm_id: int,
                              include_allowed_datatypes: bool | None = Query(description="Include the allowed datatypes"
                              "for each algorithm present in the system",default=False)):
    """
    ## `get_algorithm_by_id`

    ### Endpoint:
    `GET /{algorithm_id}`

    ### Description:
    This endpoint retrieves a specific algorithm based on the provided `algorithm_id`. You can choose whether to include the allowed data types associated with the algorithm. By default, the response will only contain the basic algorithm information, but you can request more detailed information about the allowed data types.

    ### Path Parameter:
    - `algorithm_id` (Type: `int`): The unique ID of the algorithm you want to retrieve.

    ### Query Parameters:
    - `include_allowed_datatypes` (Type: `bool | None`):
      - Optional query parameter to determine whether to include the allowed data types for the requested algorithm.
      - **Default**: `False`
      - **Description**: If set to `True`, the response will include the allowed data types for the algorithm. If `False`, only basic algorithm information is returned.

    ### Responses:
    - **200 OK**: Returns the requested algorithm along with or without allowed data types, depending on the `include_allowed_datatypes` parameter.

      If `include_allowed_datatypes=False` (default):
      - **Response Model**: A `PydanticAlgorithm` object, containing basic algorithm details.
        - **Example**:
          ```json
          {
            "id": "algorithm_id",
            "name": "algorithm_name",
            "description": "algorithm_description"
          }
          ```

      If `include_allowed_datatypes=True`:
      - **Response Model**: An `AlgorithmAndAllowedDatatypes` object, including the algorithm and its associated allowed data types.
        - **Example**:
          ```json
          {
            "id": "algorithm_id",
            "name": "algorithm_name",
            "allowed_data": [
              {
                "datatype": "datatype_name",
                "is_categorical": true
              },
              ...
            ]
          }
          ```

    - **404 Not Found**: If no algorithm is found with the specified `algorithm_id`.
      - **Response Model**: A string message indicating that the algorithm was not found.
        - **Example**:
          ```json
          {
            "message": "Algorithm not found"
          }
          ```

    ### Error Handling:
    - **404 Not Found**: If the specified algorithm ID does not exist in the database, a `404 Not Found` error is returned, along with a message like `"Algorithm not found"` or `"Algorithm not present"` depending on the situation.

    ### Database Query:
    - If `include_allowed_datatypes=False`: The function fetches the algorithm with the given `algorithm_id` and returns its basic information as a `PydanticAlgorithm` object.
    - If `include_allowed_datatypes=True`: The function performs a query to join the `Algorithm`, `AllowedDataType`, and `DataType` tables and retrieves the algorithm along with its associated allowed data types, returning the result as an `AlgorithmAndAllowedDatatypes` object.

    ### Example Flow:
    1. A GET request is made to retrieve an algorithm by its ID.
    2. If the `include_allowed_datatypes` parameter is set to `False` (or omitted), only the basic algorithm details are returned.
    3. If the `include_allowed_datatypes` parameter is set to `True`, the response will include the allowed data types for the specified algorithm.
    4. If the algorithm ID is not found, a `404 Not Found` response is returned with an error message.

    ### Example Request:
    - `GET /{algorithm_id}?include_allowed_datatypes=true`

    ### Example Response (when `include_allowed_datatypes=True`):
    ```json
    {
      "id": "algorithm_id",
      "name": "algorithm_name",
      "allowed_data": [
        {
          "datatype": "string",
          "is_categorical": true
        },
        {
          "datatype": "integer",
          "is_categorical": false
        }
      ]
    }

    """
    if not include_allowed_datatypes:
        try:
            sys_model = Algorithm.select().where(Algorithm.id == algorithm_id).dicts().get()
        except DoesNotExist:
            return JSONResponse(status_code=404,content={"message":"Algorithm not found"})
        return PydanticAlgorithm(**sys_model)
    else:
        try:
            algorithm = (Algorithm.select(
                Algorithm,
                fn.JSON_AGG(fn.JSON_BUILD_OBJECT('datatype', DataType.type, 'is_categorical', DataType.is_categorical))
                .alias("allowed_data"))
                         .join(AllowedDataType, JOIN.LEFT_OUTER)
                         .join(DataType, JOIN.LEFT_OUTER)
                         .where(Algorithm.id == algorithm_id)
                         .group_by(Algorithm.id)).dicts().get()
        except DoesNotExist:
            return JSONResponse(status_code=404, content={'message': "Algorithm not present"})
        return AlgorithmAndAllowedDatatypes(**algorithm)



@router.delete("/{algorithm_id}",
               status_code=200,
               name="Delete an algorithm given his id",
               summary="It deletes an algorithm given the id and his allowed datatypes and trained models",
               responses={404: {"model": str}})
async def delete_algorithm(algorithm_id: int):
    """
    ## `delete_algorithm`

    ### Endpoint:
    `DELETE /{algorithm_id}`

    ### Description:
    This endpoint allows you to delete a specific algorithm by its `algorithm_id`. When an algorithm is deleted, its associated allowed data types and any trained models are also removed. This ensures that all related data is cleaned up along with the algorithm.

    ### Path Parameter:
    - `algorithm_id` (Type: `int`): The unique ID of the algorithm to be deleted.

    ### Responses:
    - **200 OK**: If the algorithm, its associated allowed data types, and trained models are successfully deleted.
      - **Example Response**:
        ```json
        {
          "message": "Algorithm deleted successfully"
        }
        ```

    - **404 Not Found**: If no algorithm exists with the provided `algorithm_id`.
      - **Response Model**: A string message indicating that the algorithm was not found.
        - **Example**:
          ```json
          {
            "message": "This algorithm does not exist!"
          }
          ```

    ### Error Handling:
    - **404 Not Found**: If the algorithm with the provided `algorithm_id` does not exist, a `404 Not Found` error is returned with a message `"This algorithm does not exist!"`.

    ### Deletion Process:
    1. **Delete Allowed Data Types**: The associated allowed data types for the algorithm are deleted first by removing entries in the `AllowedDataType` table where the `algorithm_id` matches the provided `algorithm_id`.
    2. **Delete Trained Models**: All trained models related to the algorithm are identified, and for each, the corresponding trained model is deleted using the `delete_train_model` function.
    3. **Delete Algorithm**: Once the associated data is removed, the algorithm itself is deleted from the `Algorithm` table.

    ### Example Flow:
    1. A DELETE request is made to delete an algorithm by its `algorithm_id`.
    2. The system first checks if the algorithm exists in the database.
    3. If it exists, the algorithm’s associated allowed data types are deleted.
    4. Next, the trained models associated with the algorithm are deleted.
    5. Finally, the algorithm is deleted from the `Algorithm` table.
    6. If the algorithm does not exist, a `404 Not Found` response is returned with an appropriate error message.

    ### Example Request:
    - `DELETE /{algorithm_id}`

    ### Example Response (when algorithm is deleted successfully):
    ```json
    {
      "message": "Algorithm deleted successfully"
    }

    """
    try:
        algorithm = Algorithm.get_by_id(algorithm_id)
    except DoesNotExist:
        return JSONResponse(status_code=404,content={"message":"This algorithm does not exist!"})
    # First we delete the allowed datatypes
    AllowedDataType.delete().where(AllowedDataType.algorithm_id == algorithm_id).execute()
    # Then we delete all the train models associated with it
    trained_model_ids = TrainedModel.select(TrainedModel.id).where(TrainedModel.algorithm_id == algorithm_id).dicts()
    for row in trained_model_ids:
        await delete_train_model(row['id'])
    # Finally we delete the algorithm
    algorithm.delete_instance()