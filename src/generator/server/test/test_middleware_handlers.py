

model = {
    "name": "A model name",
    "size": "A model size",
    "input_shape": "(16,1)",
    "algorithm_id": 1,
    "dataset_name": "A dataset name",
}
version_info = {
    "version_name": "A version info",
    "image_path": "A posix path",
}
training_info = {
    "loss_function": "A loss function",
    "train_loss": 0,
    "val_loss": 0,
    "train_samples": 0,
    "val_samples": 0
}
feature_schema = [
    {
        "feature_name": "The name of a feature",
        "feature_position": 0,
        "is_categorical": True,
        "datatype": "string"
    }
]
model_to_save = {
    "trained_model": model,
    "version": version_info,
    "training_info": training_info,
    "feature_schema": feature_schema,
}

def test_model_to_middleware():
    pass
