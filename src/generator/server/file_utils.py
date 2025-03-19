import json
import os
from pathlib import Path
from shutil import copytree, rmtree

import pandas as pd
from loguru import logger

ROOT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUTPUT_FOLDER = os.path.join(ROOT_FOLDER, "outputs")
MODEL_FOLDER = os.path.join(OUTPUT_FOLDER, "models")
GENERATION_FOLDER = os.path.join(OUTPUT_FOLDER, "datasets")
CURRENT_FOLDER =os.path.dirname(os.path.abspath(__file__)) + "\\"

def create_folder_structure():
    if not os.path.isdir(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)
    if not os.path.isdir(MODEL_FOLDER):
        os.mkdir(MODEL_FOLDER)
    if not os.path.isdir(GENERATION_FOLDER):
        os.mkdir(GENERATION_FOLDER)


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


def create_new_version_folder(folder_path:str):
    new_version = check_folder_latest_version(folder_path) + 1
    root_folder = get_model_root_folder()
    new_version_folder = f"{root_folder}:{new_version}"
    save_folder = os.path.join(folder_path, new_version_folder)

    if not os.path.isdir(save_folder):
        os.makedirs(save_folder)

    return save_folder


def check_folder_latest_version(model_folder: str):
    root_folder = get_model_root_folder()
    my_folders_versions = [int(fold.split(":")[1]) for fold in os.listdir(model_folder) if root_folder in fold]
    if len(my_folders_versions) > 0:
        return max(my_folders_versions)
    else:
        return 0


def get_model_root_folder():
    """
    Returns the basename of the folder, formed with Class Name + Model Name
    :return:
    """
    return MODEL_FOLDER


def get_last_folder(model_folder: str):
    """
    Returns the name of the latest version image of the model
    :return:
    """
    root_folder = get_model_root_folder()
    version = check_folder_latest_version(model_folder)
    latest_version_folder = f"{root_folder}:{version}"
    return latest_version_folder


def rollback_latest_version(model_folder: str):
    last_folder = os.path.join(model_folder, get_last_folder(model_folder))
    if os.path.isdir(last_folder):
        rmtree(last_folder)
        logger.info(f"Deleted {last_folder}")


def cleanup_temp_dir(tmp_path):
    rmtree(tmp_path)

def get_all_subfolders_ids(folder_path: str) -> list:
    """
    """
    keys = []
    folders = os.walk(folder_path)
    for folder, _, _ in list(folders)[1:]:
        keys.append((folder,folder[folder.rfind('\\') + 1:]))
    return keys

def create_trained_model_folder(dest: Path,tmp_path: str):
    if os.path.isdir(dest):
        raise FileExistsError
    else:
        # This will also create the directory and move all the stuff from the temp directory
        copytree(tmp_path,dest)




def create_server_repo_folder_structure() -> None:
    """
    This function finds creates a folder structure for the all the models that are being saved on the server
    """
    server_folder = os.path.dirname(os.path.abspath(__file__))
    saved_root = os.path.join(server_folder,Path('saved_models'))
    if not os.path.isdir(saved_root):
        os.mkdir(saved_root)
        os.mkdir(os.path.join(saved_root,Path("algorithms")))
        os.mkdir(os.path.join(saved_root,Path("trained_models")))
    elif (os.path.isdir(os.path.join(saved_root ,Path("algorithms")))
          and not os.path.isdir(os.path.join(saved_root,Path("trained_models")))):
        os.mkdir(os.path.join(saved_root,Path("trained_models")))
    elif not os.path.isdir(os.path.join(saved_root,"algorithms")):
        os.mkdir(os.path.join(saved_root,Path("algorithms")))


