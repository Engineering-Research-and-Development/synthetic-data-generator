import copy

import pandas as pd

from ai_lib.Exceptions import DataException
from ai_lib.generator.evaluate.tabular_evaluate import TabularComparisonEvaluator
from ai_lib.generator.models.classes.Model import UnspecializedModel
from ai_lib.generator.models.dataset.Dataset import Dataset
from ai_lib.generator.models.model_factory import model_factory
from ai_lib.utils.file_utils import store_files


def run_train_inference_job(model: dict, behaviours: list[dict], dataset: list, n_rows:int) \
        -> tuple[list[dict], dict, UnspecializedModel, Dataset]:

    if len(dataset) == 0:
        raise DataException("To run a training instance it is necessary to pass training data")

    data = Dataset(dataset=dataset)
    input_shape = data.input_shape
    m = model_factory(model, input_shape)

    m.train(data=data)
    m.save()

    predicted_data = m.infer(n_rows)
    predicted_data = m.inverse_scale(predicted_data)

    df_predict = pd.DataFrame(data=predicted_data.tolist(),
                              columns=data.columns)

    evaluator = TabularComparisonEvaluator(real_data=data.dataframe,
                                           synthetic_data=df_predict,
                                           numerical_columns=data.continuous_columns,
                                           categorical_columns=data.categorical_columns)
    report = evaluator.compute()

    generated_data = copy.deepcopy(data)
    generated_data.dataframe = df_predict
    results = generated_data.parse_tabular_data_json()

    # Remove after debug
    store_files(m.get_last_folder(), df_predict, report)
    ######

    return results, report, m, data

