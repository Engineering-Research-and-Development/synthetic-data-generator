import numpy as np
import pandas as pd

def parse_tabular_data(data: list[dict]) -> tuple[pd.DataFrame, list[str], list[str], list[str]]:
    """
    Convert data from requests into an easy-to-process dataframe
    :param data: a list of dictionary, structured as follows:
    dataset: [{
        column_data: [ ... ],
        column_name: str,
        column_type: str [numerical/categorical],
        column_datatype: str
    }]
    :return: a pandas Dataframe where each column is structured as expected
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
        if column_type == "numerical":
            numerical_columns.append(column_name)
        elif column_type == "categorical":
            categorical_columns.append(column_name)

    # Transposing array. Since columns are appended row-wise, by transposing we obtain a column-wise data structure
    data_structure = np.array(data_structure).T
    data_frame = pd.DataFrame(data=data_structure, columns=column_names)

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
            "column_type": "numerical" if col in numerical_columns else "categorical" if col in categorical_columns
            else "None",
            "column_datatype": str(dataset[col].dtype)
        }
        for col in dataset.columns
    ]


def parse_model_info(model_dict :dict):
    model_file = model_dict.get("image", None)
    metadata = model_dict.get("metadata", {})
    model_type = model_dict.get("algorithm_name", "")
    model_name = model_dict.get("model_name", "Foo")
    input_shape = model_dict.get("input_shape", "")

    return model_file, metadata, model_type, model_name, input_shape


