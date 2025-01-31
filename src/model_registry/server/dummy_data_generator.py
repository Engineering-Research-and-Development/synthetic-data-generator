from database.schema import SystemModel, DataType, AllowedDataType, TrainedModel, Features, TrainingInfo, ModelVersion, \
    Function, Parameter, FunctionParameter


def insert_data():
    # Insert SystemModel
    systems = [
        SystemModel.create(name=f"System_{i}", description=f"Unique Description {i}", loss_function=f"LossFunction_{i}")
        for i in range(5)
    ]

    # Insert DataType
    data_types = [
        DataType.create(type=f"DataType_{i}", is_categorical=(i % 2 == 0))
        for i in range(5)
    ]

    # Insert AllowedDataType
    allowed_data_types = [
        AllowedDataType.create(algorithm_name=systems[i], datatype=data_types[(i+1) % 5])
        for i in range(5)
    ]

    # Insert TrainedModel
    trained_models = [
        TrainedModel.create(name=f"TrainedModel_{i}", dataset_name=f"Dataset_{i}", size=f"{(i+1)*15}MB",
                            input_shape=f"({i+1}x{i+2}x{i+3})", algorithm_name=systems[(i+2) % 5])
        for i in range(5)
    ]

    # Insert Features
    features = [
        Features.create(feature_name=f"Feature_{i}", datatype=data_types[(i+3) % 5], feature_position=i+10,
                        trained_model=trained_models[(i+4) % 5])
        for i in range(5)
    ]

    # Insert TrainingInfo
    training_infos = [
        TrainingInfo.create(loss_function=f"LossFunction_{i}", train_loss_value=0.1*i + 0.05, val_loss_value=0.2*i + 0.1,
                            n_train_sample=100*i + 10, n_validation_sample=50*i + 5)
        for i in range(5)
    ]

    # Insert ModelVersion
    model_versions = [
        ModelVersion.create(version_name=f"v{i+1}.0", model_image_path=f"/models/unique_model_{i}.h5",
                            trained_model=trained_models[(i+1) % 5], training_info=training_infos[(i+3) % 5])
        for i in range(5)
    ]

    # Insert Function
    functions = [
        Function.create(name=f"Function_{i}", description=f"Description for Function_{i}", function_reference=f"ref_{i}")
        for i in range(5)
    ]

    # Insert Parameter
    parameters = [
        Parameter.create(name=f"Parameter_{i}", value=f"Value_{i}", parameter_type="float")
        for i in range(5)
    ]

    # Insert FunctionParameter
    function_parameters = [
        FunctionParameter.create(function=functions[i], parameter=parameters[(i+1) % 5])
        for i in range(5)
    ]
