from models.model_factory import model_factory
import pandas as pd
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    test = {
        "model_file": "Test-T_VAE-v1",
        "model_name": "Test-T_VAE",
        "algorithm": "models.classes.keras.keras_tabular_vae.KerasTabularVAE",
        "metadata": {
            "save_filename": "Test-T_VAE-v1",
            "input_shape": "(13)",
            "model_version": "v1"
        }
    }
    m = model_factory(test)
    print(m)
    print(m.metadata)
    new_data = m.infer(1000)
    df_predict = pd.DataFrame(new_data)
    df_predict.to_csv("wine_generated_infer.csv", index=False)
    df_predict.describe()