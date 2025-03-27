from database.schema import (
    Algorithm,
    DataType,
    AlgorithmDataType,
    TrainedModel,
    TrainModelDatatype,
    ModelVersion,
    Function,
    Parameter,
    FunctionParameter,
)
import random


def insert_data():
    # Create Algorithms
    algorithms = [
        {
            "name": "Random Forest",
            "description": "Ensemble learning method",
            "default_loss_function": "gini",
        },
        {
            "name": "Neural Network",
            "description": "Deep learning model",
            "default_loss_function": "categorical_crossentropy",
        },
        {
            "name": "SVM",
            "description": "Support Vector Machine",
            "default_loss_function": "hinge",
        },
        {
            "name": "Logistic Regression",
            "description": "Linear classification",
            "default_loss_function": "log_loss",
        },
    ]

    algo_objs = []
    for algo in algorithms:
        algo_objs.append(Algorithm.create(**algo))

    # Create DataTypes
    data_types = [
        {"type": "integer", "is_categorical": False},
        {"type": "float", "is_categorical": False},
        {"type": "string", "is_categorical": True},
        {"type": "boolean", "is_categorical": True},
        {"type": "image", "is_categorical": False},
    ]

    dtype_objs = []
    for dt in data_types:
        dtype_objs.append(DataType.create(**dt))

    # Create AlgorithmDataType relationships
    for algo in algo_objs:
        # Randomly assign 2-4 data types to each algorithm
        num_types = random.randint(2, 4)
        selected_types = random.sample(dtype_objs, num_types)
        for dtype in selected_types:
            AlgorithmDataType.create(algorithm_id=algo, datatype_id=dtype)

    # Create TrainedModels
    trained_models = [
        {
            "name": "Image Classifier",
            "dataset_name": "CIFAR-10",
            "size": "50MB",
            "input_shape": "(32,32,3)",
            "algorithm_id": algo_objs[1],
        },
        {
            "name": "Fraud Detector",
            "dataset_name": "Credit Card Fraud",
            "size": "5MB",
            "input_shape": "(30,)",
            "algorithm_id": algo_objs[0],
        },
        {
            "name": "Sentiment Analyzer",
            "dataset_name": "IMDB Reviews",
            "size": "15MB",
            "input_shape": "(1000,)",
            "algorithm_id": algo_objs[3],
        },
        {
            "name": "Object Detector",
            "dataset_name": "COCO",
            "size": "120MB",
            "input_shape": "(256,256,3)",
            "algorithm_id": algo_objs[1],
        },
    ]

    model_objs = []
    for model in trained_models:
        model_objs.append(TrainedModel.create(**model))

    # Create TrainModelDatatype features
    feature_names = [
        "age",
        "income",
        "color",
        "height",
        "weight",
        "pixel",
        "text",
        "label",
        "score",
    ]
    for model in model_objs:
        num_features = random.randint(3, 7)
        for i in range(num_features):
            TrainModelDatatype.create(
                feature_name=f"{random.choice(feature_names)}_{i}",
                feature_position=i,
                datatype_id=random.choice(dtype_objs),
                trained_model_id=model,
            )

    # Create ModelVersions
    for model in model_objs:
        for v in range(1, random.randint(2, 4)):
            ModelVersion.create(
                version_name=f"v{v}.0",
                image_path=f"/models/{model.name.replace(' ', '_')}_v{v}.h5",
                loss_function=model.algorithm_id.default_loss_function,
                train_loss=random.uniform(0.1, 1.0),
                val_loss=random.uniform(0.1, 1.0),
                train_samples=random.randint(1000, 10000),
                val_samples=random.randint(200, 2000),
                trained_model_id=model,
            )

    # Create Functions
    functions = [
        {
            "name": "preprocess_image",
            "description": "Normalizes and resizes image",
            "function_reference": "image_utils.preprocess",
        },
        {
            "name": "tokenize_text",
            "description": "Tokenizes input text",
            "function_reference": "text_utils.tokenize",
        },
        {
            "name": "normalize",
            "description": "Normalizes numeric values",
            "function_reference": "math_utils.normalize",
        },
        {
            "name": "one_hot_encode",
            "description": "Encodes categorical values",
            "function_reference": "category_utils.encode",
        },
    ]

    func_objs = []
    for func in functions:
        func_objs.append(Function.create(**func))

    # Create Parameters
    parameters = [
        {"name": "target_size", "value": "256", "parameter_type": "float"},
        {"name": "mean", "value": "0.5", "parameter_type": "float"},
        {"name": "std", "value": "0.5", "parameter_type": "float"},
        {"name": "max_tokens", "value": "1000", "parameter_type": "float"},
        {"name": "min_value", "value": "0", "parameter_type": "float"},
        {"name": "max_value", "value": "1", "parameter_type": "float"},
    ]

    param_objs = []
    for param in parameters:
        param_objs.append(Parameter.create(**param))

    # Create FunctionParameter relationships
    FunctionParameter.create(
        function=func_objs[0], parameter=param_objs[0]
    )  # preprocess_image - target_size
    FunctionParameter.create(
        function=func_objs[0], parameter=param_objs[1]
    )  # preprocess_image - mean
    FunctionParameter.create(
        function=func_objs[0], parameter=param_objs[2]
    )  # preprocess_image - std
    FunctionParameter.create(
        function=func_objs[1], parameter=param_objs[3]
    )  # tokenize_text - max_tokens
    FunctionParameter.create(
        function=func_objs[2], parameter=param_objs[4]
    )  # normalize - min_value
    FunctionParameter.create(
        function=func_objs[2], parameter=param_objs[5]
    )  # normalize - max_value

    print("Successfully populated database with dummy data!")
