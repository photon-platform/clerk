import click
from trogon import tui
from .progenitor import create_project
from photon_platform.formulator import load_blueprint, Formulator

import pkg_resources


@tui()
@click.option(
    "--org_name",
    prompt="Name of the github acct/org",
    help="Name of the github acct/org",
)
@click.option(
    "--namespace", prompt="Name of the namespace", help="Name of the namespace"
)
@click.option(
    "--project_name", prompt="Name of the project", help="Name of the project"
)
@click.option("--author", prompt="Author of the project", help="Author of the project")
@click.option(
    "--path", prompt="Path to the project folder", help="Path to the project folder"
)
@click.command()
def run(org_name, namespace, project_name, author, path):
    """Create a new Python project in an empty folder."""
    create_project(org_name, namespace, project_name, author, path)


if __name__ == "__main__":
    run()
