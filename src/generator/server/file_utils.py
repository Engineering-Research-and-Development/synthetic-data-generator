import os
from pathlib import Path
from shutil import copytree, rmtree

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
TRAINED_MODELS = Path(APP_FOLDER) / "saved_models" / "trained_models"


def cleanup_temp_dir(tmp_path):
    rmtree(tmp_path)


def get_all_subfolders_ids(folder_path: str) -> list:
    keys = []
    folders = os.walk(folder_path)
    for folder, _, _ in list(folders)[1:]:
        keys.append((folder, folder[folder.rfind("\\") + 1 :]))
    return keys


def create_trained_model_folder(dest: Path, tmp_path: str):
    copytree(tmp_path, dest)


def create_server_repo_folder_structure() -> None:
    """
    Creates a folder structure for saving models on the server.

    The structure includes:
    - saved_models/
      - trained_models/
    """
    TRAINED_MODELS.mkdir(parents=True, exist_ok=True)
