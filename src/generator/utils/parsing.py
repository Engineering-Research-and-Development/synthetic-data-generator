from generator.models.classes.Model import UnspecializedModel
from generator.models.dataset.Dataset import Dataset


def parse_model_info(model_dict :dict):
    model_file = model_dict.get("image", None)
    metadata = model_dict.get("metadata", {})
    model_type = model_dict.get("algorithm_name", None)
    model_name = model_dict.get("model_name", None)
    input_shape = model_dict.get("input_shape", "")

    return model_file, metadata, model_type, model_name, input_shape


def parse_model_to_registry(model: UnspecializedModel, data: Dataset):

    feature_list = data.parse_data_to_registry()
    training_info = model.training_info.__dict__
    model_image = model.model_filepath
    model_version = model.check_folder_latest_version()
    version_info = {"version_name": model_version, "model_image_path": model_image}
    trained_model_misc = {
        "name": model.model_name,
        "size": model.self_describe().get("size", "Not Available"),
        "input_shape": str(model.input_shape),
        "algorithm_name": model.self_describe().get("name", None)
    }

    model_to_save = {
        "trained_model": trained_model_misc,
        "version": version_info,
        "training_info": training_info,
        "feature_schema": feature_list
    }
    return model_to_save

