import copy
import pandas as pd

from ai_lib.Exceptions import ModelException
from ai_lib.data_generator.evaluate.TabularComparison import TabularComparisonEvaluator
from ai_lib.Dataset import Dataset
from ai_lib.data_generator.model_factory import model_factory
from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel


def job(model_info: dict, dataset: list, n_rows:int, save_filepath:str, train:bool) \
        -> tuple[list[dict], dict, UnspecializedModel, Dataset]:

    if len(dataset) == 0:
        data_info = model_info.get("training_data_info", [])
        if len(data_info) == 0:
            raise ModelException("It is not possible to infer column names from model")
        data = Dataset(dataset=data_info)
    else:
        data = Dataset(dataset=dataset)

    model = model_factory(model_info, data.input_shape)
    if train:
        model.train(data=data)
        model.save(save_filepath)

    predicted_data = model.infer(n_rows)
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

    return results, report, model, data