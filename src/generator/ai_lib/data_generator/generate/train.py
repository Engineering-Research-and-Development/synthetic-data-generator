import copy

import pandas as pd
from ai_lib.data_generator.evaluate.TabularComparison import TabularComparisonEvaluator
from ai_lib.data_generator.models.UnspecializedModel import UnspecializedModel
from ai_lib.Dataset import Dataset
from ai_lib.data_generator.model_factory import model_factory


def run_train_inference_job(model: dict, behaviours: list[dict], dataset: list, n_rows:int) \
        -> tuple[list[dict], dict, UnspecializedModel, Dataset]:

    data = Dataset(dataset=dataset)
    input_shape = data.input_shape
    model = model_factory(model, input_shape)

    model.train(data=data)
    model.save()

    predicted_data = model.infer(n_rows)
    predicted_data = model._inverse_scale(predicted_data)

    df_predict = pd.DataFrame(data=predicted_data.tolist(), columns=data.columns)

    evaluator = TabularComparisonEvaluator(real_data=data.dataframe,
                                           synthetic_data=df_predict,
                                           numerical_columns=data.continuous_columns,
                                           categorical_columns=data.categorical_columns)
    metrics = evaluator.compute()

    generated_data = copy.deepcopy(data)
    generated_data.dataframe = df_predict
    results = generated_data.parse_tabular_data_json()

    return results, metrics, model, data

