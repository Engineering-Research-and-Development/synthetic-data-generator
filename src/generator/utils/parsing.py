import numpy as np
import pandas as pd

def parse_tabular_data(data: list[dict]) -> tuple[pd.DataFrame, list[str], list[str]]:
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

    return data_frame, categorical_columns, numerical_columns

