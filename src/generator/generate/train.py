from models.model_factory import model_factory
import pandas as pd
from sklearn.preprocessing import StandardScaler
from evaluate.tabular_evaluate import TabularComparisonEvaluator

import json

if __name__ == "__main__":
    test = {
        "image": "",
        "model_name": "Test-T_VAE",
        "model_version": "v1",
        "algorithm_name": "models.classes.keras.keras_tabular_vae.KerasTabularVAE",
        "metadata": {
            "input_shape": "(13)",
        }
    }
    column_names = ['alcohol','malic_acid','ash','acl', 'Mmg', 'phenols', 'flavanoids','nonflavanoid_phenols',
                    'proanth','color_int','hue', 'od','prolin']
    m = model_factory(test)
    csv_data = pd.read_csv("wine_clean.csv", header=None)
    csv_data.columns = column_names
    data = csv_data.values

    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    m.scaler = scaler
    m.train(data)
    df_normalized = pd.DataFrame(data)
    df_normalized.to_csv("wine_norm.csv", index=False)
    print(m)
    print(m.metadata)
    #m.save()
    new_data = m.infer(1000)
    new_data = scaler.inverse_transform(new_data)
    df_predict = pd.DataFrame(new_data)
    df_predict.columns = column_names
    evaluator = TabularComparisonEvaluator(csv_data, df_predict, column_names, [])
    report = evaluator.compute()
    print(json.dumps(report))
    df_predict.to_csv("wine_generated.csv", index=False)
    df_predict.describe()