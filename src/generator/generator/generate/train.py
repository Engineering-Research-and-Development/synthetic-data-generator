import copy

from exceptions.DataException import DataException
from generator.models.classes.Model import UnspecializedModel
from generator.models.dataset.Dataset import Dataset
from generator.models.model_factory import model_factory
from utils.file_utils import store_files
import pandas as pd
from generator.evaluate.tabular_evaluate import TabularComparisonEvaluator


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
    predicted_data = m.scaler.inverse_transform(predicted_data)

    df_predict = pd.DataFrame(data=predicted_data,
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

