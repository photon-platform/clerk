"""The package entry point into the application."""

import click
from photon_platform.progenitor import create_project


@click.command()
@click.option("--github_id", prompt="Github ID", help="Github Org or Personal ID")
@click.option(
    "--package_namespace",
    prompt="Package Namespace",
    help="Namespace for Python modules",
)
@click.option("--github_repo_id", prompt="Repo ID", help="Name of the github repo")
@click.option("--package_name", prompt="Package Name", help="Name for Python package")
@click.option("--author", prompt="Author", help="ID of author")
@click.option("--description", prompt="Description", help="Short statement on the project")
@click.option(
    "--path",
    default=".",
    help="Path to create the project in.",
)
def run(
    github_id,
    package_namespace,
    github_repo_id,
    package_name,
    author,
    description,
    path,
):
    """Create a new Python project in an empty folder."""
    create_project(
        github_id,
        package_namespace,
        github_repo_id,
        package_name,
        author,
        description,
        path,
    )


if __name__ == "__main__":
    run()
