from models.model_factory import model_factory
import pandas as pd
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    test = {
        "model_file": "",
        "algorithm": "models.classes.keras.keras_tabular_vae.KerasTabularVAE",
        "metadata": {
            "input_shape": "(13)"
        }
    }
    m = model_factory(test)
    csv = pd.read_csv("wine_clean.csv")
    data = csv.values

    scaler = StandardScaler()
    data = scaler.fit_transform(data)
    m.train(data)
    print(m)
    print(m.metadata)
    new_data = m.infer(1000)
    new_data = scaler.inverse_transform(new_data)
    df_predict = pd.DataFrame(new_data)
    df_predict.to_csv("wine_generated.csv", index=False)