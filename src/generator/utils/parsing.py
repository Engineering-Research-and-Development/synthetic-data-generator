from enum import CONTINUOUS

import numpy as np
import pandas as pd

from exceptions.DataException import DataException
from models.classes.Model import UnspecializedModel

NUMERICAL = "continuous"
CATEGORICAL = "categorical"


def parse_tabular_data(data: list[dict]) -> tuple[pd.DataFrame, list[str], list[str], list[str]]:
    """
    Convert data from requests into an easy-to-process dataframe
    :param data: a list of dictionary, structured as follows:
    dataset: [{
        column_data: [ ... ],
        column_name: str,
        column_type: str [continuous/categorical],
        column_datatype: str
    }]
    :return: a pandas Dataframe where each column is structured as expected
    :raises: DataException
    """
    column_names = []
    categorical_columns = []
    numerical_columns = []
    data_structure = []
    for col in data:
        content = col.get("column_data", [])
        content_type = col.get("column_datatype", "object")
        column_name = col.get("column_name", "")
        column_type = col.get("column_type", "")
        data_structure.append(np.array(content, dtype=content_type))
        column_names.append(column_name)
        if column_type == NUMERICAL:
            numerical_columns.append(column_name)
        elif column_type == CATEGORICAL:
            categorical_columns.append(column_name)

    # Transposing array. Since columns are appended row-wise, by transposing we obtain a column-wise data structure
    data_structure = np.array(data_structure).T
    data_frame = pd.DataFrame(data=data_structure, columns=column_names)

    if len(column_names) < 1:
        raise DataException("No column names are passed to the input data")

    return data_frame, column_names, numerical_columns, categorical_columns



def parse_tabular_data_json(dataset: pd.DataFrame, numerical_columns:list[str], categorical_columns:list[str]) -> list[dict]:
    """
    Converts data from a dataframe into a list of dictionaries
    :param dataset: the pandas dataframe to be converted
    :param numerical_columns: the names of the numerical columns
    :param categorical_columns: the names of the categorical colums
    :return: a dictionary in form of:
    dataset: [{
        column_data: [ ... ],
        column_name: str,
        column_type: str [numerical/categorical],
        column_datatype: str
    }]
    """
    return [
        {
            "column_data" : dataset[col].to_numpy().tolist(),
            "column_name": col,
            "column_type": NUMERICAL if col in numerical_columns else CATEGORICAL if col in categorical_columns
            else "None",
            "column_datatype": str(dataset[col].dtype)
        }
        for col in dataset.columns
    ]


def parse_data_to_registry(data: list[dict]) -> list[dict]:
    """
    Translates data structure from input coherence to a structured
    :param data:
    :return:
    """
    feature_list = []
    for idx, col in enumerate(data):
        feat = {
            "feature_name" : col.get("column_name", ""),
            "feature_position": idx,
            "is_categorical": True if col.get("column_type", "") == CATEGORICAL else False,
            "datatype": col.get("column_datatype", "")
        }
        feature_list.append(feat)
    return feature_list


def parse_model_info(model_dict :dict):
    model_file = model_dict.get("image", None)
    metadata = model_dict.get("metadata", {})
    model_type = model_dict.get("algorithm_name", None)
    model_name = model_dict.get("model_name", None)
    input_shape = model_dict.get("input_shape", "")

    return model_file, metadata, model_type, model_name, input_shape


def parse_model_to_registry(model_dict: dict, model: UnspecializedModel, data: list[dict]):

    model_file, metadata, model_type, model_name, input_shape = parse_model_info(model_dict)
    feature_list = parse_data_to_registry(data)
    training_info = model.metadata.get("training_info", {})
    model_image = model.model_filepath
    model_version = model.check_folder_latest_version()
    version_info = {"version_name": model_version, "model_image_path": model_image}
    trained_model_misc = {
        "name": model.model_name,
        "size": "None",
        "input_shape": str(model.input_shape),
        "algorithm_name": model.self_describe().get("name", model_type)
    }

    model_to_save = {
        "trained_model": trained_model_misc,
        "version": version_info,
        "training_info": training_info,
        "feature_schema": feature_list
    }
    return model_to_save

