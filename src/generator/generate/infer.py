from evaluate.tabular_evaluate import TabularComparisonEvaluator
from exceptions.ModelException import ModelException
from models.model_factory import model_factory
import pandas as pd

from utils.parsing import parse_tabular_data, parse_tabular_data_json

def run_infer_job(model: dict, behaviours: list[dict], dataset: list, n_rows:int) -> tuple[list[dict], dict]:
    if len(dataset) == 0:
        dataset = model.get("metadata", {}).get("training_data_info", [])
        print(dataset)
        if len(dataset) == 0:
            raise ModelException("It is not possible to infer column names")

    dataframe, columns, numerical_columns, categorical_columns = parse_tabular_data(data=dataset)
    np_input = dataframe.to_numpy()
    input_shape = str(np_input.shape[1:])

    m = model_factory(model, input_shape)
    predicted_data = m.infer(n_rows)
    predicted_data = m.scaler.inverse_transform(predicted_data)
    df_predict = pd.DataFrame(data=predicted_data,
                              columns=columns)

    report = {"available": False}
    if len(dataframe) > 0:
        evaluator = TabularComparisonEvaluator(real_data=dataframe,
                                               synthetic_data=df_predict,
                                               numerical_columns=numerical_columns,
                                               categorical_columns=categorical_columns)
        report = evaluator.compute()

    results = parse_tabular_data_json(dataset=df_predict,
                                      numerical_columns=numerical_columns,
                                      categorical_columns=categorical_columns)
    return results, report
