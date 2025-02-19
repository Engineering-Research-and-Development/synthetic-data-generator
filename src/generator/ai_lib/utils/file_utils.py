import json
import pandas as pd
import os

from server.utils import GENERATION_FOLDER


def store_files(gen_name: str, dataset: pd.DataFrame, metrics: dict):
    dir_path = os.path.join(GENERATION_FOLDER, gen_name)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    dataset_path = os.path.join(dir_path, "generation.csv")
    report_path = os.path.join(dir_path, "report.json")

    dataset.to_csv(dataset_path)

    if metrics is not None:
        with open(report_path, "w") as f:
            json.dump(metrics, f, indent=6)


