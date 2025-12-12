import os
import subprocess
from pathlib import Path
import click
from .progenitor import create_project

@click.command()
@click.argument('project_name')
@click.option('--description', '-d', help='Project description')
@click.pass_context
def init(ctx, project_name, description):
    """Creates a new Python project."""
    context = ctx.obj.get('context')
    
    if not context or not context.org_name:
         click.echo("Could not detect Organization context. Please ensure you are in ~/PROJECTS/<org>.")
         return

    github_id = context.org_name
    package_namespace = github_id.replace('-', '_')
    
    # We want to create the project in the current directory (which should be the Org dir)
    path = Path(os.getcwd())
    
    try:
        author = subprocess.check_output(['git', 'config', 'user.name']).decode('utf-8').strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        author = "phi ARCHITECT"

    # create_project signature:
    # github_id, package_namespace, github_repo_id, package_name, author, description, path
    create_project(github_id, package_namespace, project_name, project_name, author, description, str(path))
