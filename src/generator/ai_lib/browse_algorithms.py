import os
from pathlib import Path
import importlib
from typing import Generator

base_package = "ai_lib.data_generator.models."
base_model_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data_generator/models/"
)


def find_implementations(
    root_path: str, implementation_folder: str = "implementation"
) -> list[str]:
    """
    Takes a root path and a name of a folder. Returns all modules existing in each of the so-named folders
    :param implementation_folder: folder name where implemented modules exist
    :param root_path: root path in which to explore
    :return: list of stringed modules represented in py-like dot-notation
    """

    root_dir = Path(root_path).resolve()  # Ensure absolute path
    implementation_dirs = root_dir.rglob(
        implementation_folder
    )  # Find all 'implementation' folders
    module_paths = []

    for impl_dir in implementation_dirs:
        py_files = [
            file for file in impl_dir.glob("*.py") if file.name != "__init__.py"
        ]

        for file in py_files:
            rel_path = file.relative_to(root_dir).with_suffix("")  # Remove extension
            module_path = ".".join(rel_path.parts)  # Convert to module notation
            module_paths.append(module_path)

    return module_paths


def browse_algorithms(
    model_paths: str = base_model_path, model_package: str = base_package
) -> Generator[dict | None, None, None]:
    """
    Generator function to iterate.
    It exploits the find_implementations function to gather all module names, then extract from each module
    the main class. Each main class so extracted provides a dictionary description.

    :return: dictionary description of each implementation existing in ai_lib
    """

    modules = find_implementations(model_paths)
    list_module_names = [f"{model_package}{module}" for module in modules]

    for module_name in list_module_names:
        class_name = module_name.split(".")[-1]
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            yield None
            continue
        Class = getattr(module, class_name)

        yield Class.self_describe()
