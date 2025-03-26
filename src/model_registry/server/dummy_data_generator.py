from database.schema import (
    Algorithm,
    DataType,
    AlgorithmDataType,
    TrainedModel,
    TrainModelDatatype,
    TrainingInfo,
    ModelVersion,
    Function,
    Parameter,
    FunctionParameter,
)


def insert_data():
    # Insert SystemModel
    systems = [
        Algorithm.create(
            name=f"System_{i}",
            description=f"Unique Description {i}",
            default_loss_function=f"LossFunction_{i}",
        )
        for i in range(5)
    ]

    # Insert DataType
    data_types = [
        DataType.create(type=f"DataType_{i}", is_categorical=(i % 2 == 0))
        for i in range(5)
    ]

    # Insert AllowedDataType
    _ = [
        AlgorithmDataType.create(
            algorithm_id=systems[i], datatype=data_types[(i + 1) % 5]
        )
        for i in range(5)
    ]

    # Insert TrainedModel
    trained_models = [
        TrainedModel.create(
            name=f"TrainedModel_{i}",
            dataset_name=f"Dataset_{i}",
            size=f"{(i + 1) * 15}MB",
            input_shape=f"({i + 1},{i + 2},{i + 3})",
            algorithm_id=systems[(i + 1) % 5],
        )
        for i in range(5)
    ]

    # Insert Features
    _ = [
        TrainModelDatatype.create(
            feature_name=f"Feature_{i}",
            datatype=data_types[(i + 3) % 5],
            feature_position=i + 10,
            trained_model=trained_models[(i + 4) % 5],
        )
        for i in range(5)
    ]

    # Insert ModelVersion
    model_versions = [
        ModelVersion.create(
            version_name=f"v{i + 1}.0",
            image_path=f"unique_model_{i}.h5",
            trained_model=trained_models[(i + 1) % 5],
        )
        for i in range(5)
    ]
    # Inserting multiple model version for the same training model
    multiple_model_versions = [
        ModelVersion.create(
            version_name=f"v{i + 1}.0",
            image_path=f"unique_model_{i}.h5",
            trained_model=1,
        )
        for i in range(5, 9)
    ]

    all_versions = model_versions + multiple_model_versions

    # Insert TrainingInfo
    _ = [
        TrainingInfo.create(
            loss_function=f"LossFunction_{index}",
            train_loss=0.1 * index + 0.05,
            val_loss=0.2 * index + 0.1,
            train_samples=100 * index + 10,
            val_samples=50 * index + 5,
            model_version_id=i,
        )
        for index, i in enumerate(all_versions)
    ]

    # Insert Function
    functions = [
        Function.create(
            name=f"Function_{i}",
            description=f"Description for Function_{i}",
            function_reference=f"ref_{i}",
        )
        for i in range(5)
    ]

    # Insert Parameter
    parameters = [
        Parameter.create(
            name=f"Parameter_{i}", value=f"Value_{i}", parameter_type="float"
        )
        for i in range(5)
    ]

    # Insert FunctionParameter
    _ = ["int", "float", "string"]
    _ = [
        FunctionParameter.create(
            function=functions[i], parameter=parameters[(i + 1) % 5]
        )
        for i in range(5)
    ]
