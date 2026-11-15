import shutil
from datetime import date
from pathlib import Path

import yaml
from jinja2 import Environment, PackageLoader

from photon_platform.clerk.build.modulator import Modulator


def _copy_brand_assets(
    project_path: Path,
    github_id: str,
    package_namespace: str,
    script_dir: Path,
) -> None:
    """Copy canonical org logo.png and favicon.ico into docsrc/_static/."""
    tokens = {str(github_id).strip().lower(), str(package_namespace).strip().lower()}
    org_key = "geometor" if "geometor" in tokens else "photon-platform"
    assets_dir = script_dir / "assets" / org_key
    target_static = project_path / "docsrc" / "_static"
    target_static.mkdir(parents=True, exist_ok=True)
    for filename in ("logo.png", "favicon.ico"):
        src = assets_dir / filename
        if src.is_file():
            shutil.copy2(src, target_static / filename)


def create_project(
    github_id,
    package_namespace,
    github_repo_id,
    package_name,
    author,
    description,
    path,
):
    """Create a new Python project in an empty folder."""
    project_path = Path(path) / package_name

    if not project_path.exists():
        project_path.mkdir(parents=True)
    else:
        print(f"Error: The path {project_path} already exists.")
        return

    # create module stubs
    modulator = Modulator(project_path, package_namespace)
    modulator.create_module(package_name)

    # generate templates
    env = Environment(
        loader=PackageLoader("photon_platform.clerk.init"),
    )
    template_variables = {
        "author": author,
        "github_id": github_id,
        "github_repo_id": github_repo_id,
        "package_namespace": package_namespace,
        "package_name": package_name,
        "description": description,
        "init": date.today().strftime("%Y.%j"),
    }

    script_dir = Path(__file__).parent.absolute()
    yaml_file_path = script_dir / "templates.yaml"

    with open(yaml_file_path, encoding="utf-8") as f:
        file_structure = yaml.safe_load(f)

    for file_info in file_structure:
        target = project_path / file_info["target"]
        target.parent.mkdir(
            parents=True, exist_ok=True
        )  # create directory if it doesn't exist
        template = env.get_template(file_info["template"])
        target.write_text(template.render(template_variables), encoding="utf-8")

    _copy_brand_assets(project_path, github_id, package_namespace, script_dir)

