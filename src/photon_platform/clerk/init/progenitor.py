import yaml
from pathlib import Path
from jinja2 import Environment, PackageLoader
from datetime import date
from photon_platform.clerk.build.modulator import Modulator


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
        "init": date.today().strftime("%Y.%j")
    }

    script_dir = Path(__file__).parent.absolute()
    yaml_file_path = script_dir / "templates.yaml"

    with open(yaml_file_path, "r") as f:
        file_structure = yaml.safe_load(f)

    for file_info in file_structure:
        target = project_path / file_info["target"]
        target.parent.mkdir(
            parents=True, exist_ok=True
        )  # create directory if it doesn't exist
        template = env.get_template(file_info["template"])
        target.write_text(template.render(template_variables))
