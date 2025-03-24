from server.file_utils import (
    cleanup_temp_dir,
    get_all_subfolders_ids,
    create_trained_model_folder,
    create_server_repo_folder_structure,
    TRAINED_MODELS,
)


def test_create_server_repo_folder_structure(tmp_path):
    _ = tmp_path / "saved_models" / "trained_models"
    create_server_repo_folder_structure()
    assert TRAINED_MODELS.exists() and TRAINED_MODELS.is_dir()


def test_get_all_subfolders_ids(tmp_path):
    # Create test folders
    (tmp_path / "folder1").mkdir()
    (tmp_path / "folder2").mkdir()

    subfolders = get_all_subfolders_ids(str(tmp_path))

    assert len(subfolders) == 2
    assert any("folder1" in subfolder for _, subfolder in subfolders)
    assert any("folder2" in subfolder for _, subfolder in subfolders)


def test_create_trained_model_folder(tmp_path):
    src = tmp_path / "src_folder"
    dest = tmp_path / "dest_folder"
    src.mkdir()
    (src / "test_file.txt").write_text("test content")

    create_trained_model_folder(dest, str(src))

    assert dest.exists()
    assert (dest / "test_file.txt").exists()


def test_cleanup_temp_dir(tmp_path):
    temp_dir = tmp_path / "temp_to_remove"
    temp_dir.mkdir()
    assert temp_dir.exists()

    cleanup_temp_dir(temp_dir)
    assert not temp_dir.exists()
