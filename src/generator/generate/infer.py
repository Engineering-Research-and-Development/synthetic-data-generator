from evaluate.tabular_evaluate import TabularComparisonEvaluator
from models.model_factory import model_factory
import pandas as pd
import os

from utils.parsing import parse_tabular_data, parse_tabular_data_json
from utils.structure import MODEL_FOLDER

def run_infer_job(model: dict, behaviours: list[dict], dataset: list, n_rows:int) -> tuple[list[dict], dict]:
    if len(dataset) == 0:
        dataset = model.get("training_data_info", [])
        if len(dataset) == 0:
            raise ValueError("It is not possible to infer column names")

    dataframe, columns, numerical_columns, categorical_columns = parse_tabular_data(data=dataset)
    np_input = dataframe.to_numpy()
    input_shape = str(np_input.shape[1:])

    m = model_factory(model)
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

if __name__ == "__main__":

    model_folder = os.path.join(MODEL_FOLDER, "Test-T_VAE:1")
    print(model_folder)
    test = {
        "image": model_folder,
        "model_name": "Test-T_VAE",
        "model_version": "v1",
        "algorithm_name": "models.classes.keras.keras_tabular_vae.KerasTabularVAE",
        "metadata": {
            "input_shape": "(13)",
        }
    }
    m = model_factory(test)
    print(m)
    print(m.scaler)
    print(m.metadata)
    new_data = m.infer(1000)
    df_predict = pd.DataFrame(m.scaler.inverse_transform(new_data))
    df_predict.to_csv("wine_generated_infer.csv", index=False)
    df_predict.describe()