from preprocess.scale import scale_input
from models.model_factory import model_factory
from utils.parsing import parse_tabular_data, parse_tabular_data_json
import pandas as pd
from evaluate.tabular_evaluate import TabularComparisonEvaluator


def run_train_inference_job(model: dict, behaviours: list[dict], dataset: list, n_rows:int) -> tuple[list[dict], dict]:
    if len(dataset) == 0:
        raise ValueError("Training data missing")

    dataframe, columns, numerical_columns, categorical_columns =  parse_tabular_data(data=dataset)
    np_input = dataframe.to_numpy()
    input_shape = str(np_input.shape[1:])
    m = model_factory(model, input_shape)
    scaler, np_input_scaled, _ = scale_input(train_data=np_input)
    m.scaler = scaler
    m.train(data=np_input_scaled)
    m.save()
    predicted_data = m.infer(n_rows)
    predicted_data = scaler.inverse_transform(predicted_data)
    df_predict = pd.DataFrame(data=predicted_data,
                              columns=columns)
    evaluator = TabularComparisonEvaluator(real_data=dataframe,
                                           synthetic_data=df_predict,
                                           numerical_columns=numerical_columns,
                                           categorical_columns=categorical_columns)
    report = evaluator.compute()
    results = parse_tabular_data_json(dataset=df_predict,
                                      numerical_columns=numerical_columns,
                                      categorical_columns=categorical_columns)
    return results, report

