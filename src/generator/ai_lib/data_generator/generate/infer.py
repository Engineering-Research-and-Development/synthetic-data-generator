import copy

import pandas as pd

from ai_lib.Exceptions import ModelException
from ai_lib.data_generator.evaluate.TabularComparison import TabularComparisonEvaluator
from ai_lib.Dataset import Dataset
from ai_lib.data_generator.model_factory import model_factory


def run_infer_job(model: dict, behaviours: list[dict], dataset: list, n_rows:int) -> tuple[list[dict], dict]:
    if len(dataset) == 0:
        dataset = model.get("training_data_info", [])
        print(dataset)
        if len(dataset) == 0:
            raise ModelException("It is not possible to infer column names")

    data = Dataset(dataset=dataset)

    m = model_factory(model, data.input_shape)
    predicted_data = m.infer(n_rows)
    predicted_data = m.inverse_scale(predicted_data)
    df_predict = pd.DataFrame(data=predicted_data.tolist(),
                              columns=data.columns)

    report = {"available": False}
    if len(data.dataframe) > 0:
        evaluator = TabularComparisonEvaluator(real_data=data.dataframe,
                                               synthetic_data=df_predict,
                                               numerical_columns=data.continuous_columns,
                                               categorical_columns=data.categorical_columns)
        report = evaluator.compute()

    generated = copy.deepcopy(data)
    generated.dataframe = df_predict

    results = generated.parse_tabular_data_json()

    return results, report