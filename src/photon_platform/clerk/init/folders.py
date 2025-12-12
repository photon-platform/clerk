import os
from pathlib import Path


def get_base_project_folder() -> Path:
    """
    Retrieve the base project folder from an environment variable or default to '~/PROJECTS'.

    Returns:
    - Path: A pathlib.Path object representing the base project folder.
    """
    base_folder_path = os.environ.get("PHOTON_PROJECTS_BASE", "~/PROJECTS")
    base_folder_path = Path(base_folder_path).expanduser()

    if not base_folder_path.exists():
        print(f"The directory {base_folder_path} does not exist. Creating it now.")
        base_folder_path.mkdir(parents=True)

    return base_folder_path


def list_organization_folders(base_folder_path: str) -> list[str]:
    """
    List the GitHub organization folders present in the base project folder.

    Parameters:
    - base_folder_path (Path): A pathlib.Path object representing the base project folder.

    Returns:
    - list[str]: A list of folder names representing GitHub organizations.
    """
    return [f.name for f in base_folder_path.iterdir() if f.is_dir()]


if __name__ == "__main__":
    base_folder = get_base_project_folder()
    org_folders = list_organization_folders(base_folder)

    print(f"{base_folder=}")
    print(f"{org_folders=}")
