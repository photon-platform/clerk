"""
clerk
"""
import click
from pathlib import Path
from .modulator.modulator import Modulator
from .curator import curator as curator_actions
from .gather import gather as gather_actions
from .logger.logger import Logger

@click.group()
def cli():
    """A command-line tool for situational awareness and context-sensitive operations."""
    pass

@cli.group()
def gather():
    """Gathers content from various sources."""
    pass

@gather.command('url')
@click.argument('url_string')
def gather_url(url_string):
    """Gathers content from a URL, intelligently handling the source."""
    gather_actions.action_gather_url(url_string)

@gather.command('repo')
@click.argument('repo_string')
def gather_repo(repo_string):
    """Gathers information about a GitHub repository."""
    gather_actions.action_gather_repo(repo_string)


@cli.command()
def logger():
    """Creates a new log entry."""
    app = Logger()
    reply = app.run()
    print(reply)

@cli.command()
@click.option('--project-name', prompt='Project Name', help='The name of the project.')
@click.option('--description', prompt='Description', help='A short description of the project.')
def progenitor(project_name, description):
    """Creates a new Python project."""
    from .progenitor.progenitor import create_project
    import os
    import subprocess

    path = Path(os.getcwd())
    github_id = path.name
    package_namespace = github_id.replace('-', '_')
    
    try:
        author = subprocess.check_output(['git', 'config', 'user.name']).decode('utf-8').strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        author = "phi ARCHITECT"

    create_project(github_id, package_namespace, project_name, project_name, author, description, str(path))

@cli.group()
def modulator():
    """Shapes Python modules and packages."""
    pass

@modulator.command('create-module')
@click.option('--project-path', prompt='Project Path', help='The path to the project.')
@click.option('--namespace', prompt='Namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the module.')
def create_module(project_path, namespace, module_name):
    """Creates a new Python module."""
    modulator = Modulator(Path(project_path), namespace)
    modulator.create_module(module_name)
    click.echo(f"Module {module_name} created successfully.")

@modulator.command('create-submodule')
@click.option('--project-path', prompt='Project Path', help='The path to the project.')
@click.option('--namespace', prompt='Namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the parent module.')
@click.option('--submodule-name', prompt='Submodule Name', help='The name of the submodule.')
def create_submodule(project_path, namespace, module_name, submodule_name):
    """Creates a new Python submodule."""
    modulator = Modulator(Path(project_path), namespace)
    modulator.create_submodule(module_name, submodule_name)
    click.echo(f"Submodule {submodule_name} created successfully in {module_name}.")

@modulator.command('create-class')
@click.option('--project-path', prompt='Project Path', help='The path to the project.')
@click.option('--namespace', prompt='Namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the module.')
@click.option('--class-name', prompt='Class Name', help='The name of the class.')
def create_class(project_path, namespace, module_name, class_name):
    """Creates a new Python class."""
    modulator = Modulator(Path(project_path), namespace)
    modulator.create_class(module_name, class_name)
    click.echo(f"Class {class_name} created successfully in {module_name}.")

@modulator.command('create-function')
@click.option('--project-path', prompt='Project Path', help='The path to the project.')
@click.option('--namespace', prompt='Namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the module.')
@click.option('--function-name', prompt='Function Name', help='The name of the function.')
@click.option('--args', prompt='Arguments', help='The arguments for the function.')
@click.option('--return-type', prompt='Return Type', help='The return type of the function.')
def create_function(project_path, namespace, module_name, function_name, args, return_type):
    """Creates a new Python function."""
    modulator = Modulator(Path(project_path), namespace)
    modulator.create_function(module_name, function_name, args, return_type)
    click.echo(f"Function {function_name} created successfully in {module_name}.")

@modulator.command('create-class-method')
@click.option('--project-path', prompt='Project Path', help='The path to the project.')
@click.option('--namespace', prompt='Namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the module.')
@click.option('--class-name', prompt='Class Name', help='The name of the class.')
@click.option('--method-name', prompt='Method Name', help='The name of the method.')
@click.option('--args', prompt='Arguments', help='The arguments for the method.')
@click.option('--return-type', prompt='Return Type', help='The return type of the method.')
def create_class_method(project_path, namespace, module_name, class_name, method_name, args, return_type):
    """Creates a new Python class method."""
    modulator = Modulator(Path(project_path), namespace)
    modulator.create_class_method(module_name, class_name, method_name, args, return_type)
    click.echo(f"Method {method_name} created successfully in class {class_name}.")


cli.add_command(modulator)

@cli.group()
def curator():
    """Organizes git/archive management."""
    pass

@curator.command('branches')
@click.option('--repo-path', default='.', help='The path to the repository.')
def branches(repo_path):
    """Lists the branches in the repository."""
    repo = curator_actions.action_get_repo(repo_path)
    branches = curator_actions.action_get_branches(repo)
    for branch, is_active in branches.items():
        if is_active:
            click.echo(f"* {branch}")
        else:
            click.echo(f"  {branch}")

@curator.command('create-release-branch')
@click.option('--repo-path', default='.', help='The path to the repository.')
@click.option('--release-version', prompt='Release Version', help='The version number for the release.')
@click.option('--description', prompt='Description', help='A short description of the release.')
def create_release_branch(repo_path, release_version, description):
    """Creates a new release branch."""
    repo = curator_actions.action_get_repo(repo_path)
    success, message = curator_actions.action_create_release_branch(repo, release_version, description)
    if success:
        click.echo(message)
    else:
        click.echo(f"Error: {message}")

@curator.command('merge-to-main')
@click.option('--repo-path', default='.', help='The path to the repository.')
@click.option('--branch-name', prompt='Branch Name', help='The name of the branch to merge.')
@click.option('--commit-message', prompt='Commit Message', help='The commit message.')
def merge_to_main(repo_path, branch_name, commit_message):
    """Merges a branch to main."""
    repo = curator_actions.action_get_repo(repo_path)
    success, message = curator_actions.action_merge_to_main(repo, branch_name, commit_message)
    if success:
        click.echo(message)
    else:
        click.echo(f"Error: {message}")

@curator.command('create-tag')
@click.option('--repo-path', default='.', help='The path to the repository.')
@click.option('--tag-name', prompt='Tag Name', help='The name of the tag.')
@click.option('--message', prompt='Message', help='The message for the tag.')
def create_tag(repo_path, tag_name, message):
    """Creates a new tag."""
    repo = curator_actions.action_get_repo(repo_path)
    success, message = curator_actions.action_create_tag(repo, tag_name, message)
    if success:
        click.echo(message)
    else:
        click.echo(f"Error: {message}")

@curator.command('init')
def init_repo():
    """Initializes a new git repository."""
    from .curator import git_init
    git_init.main()

cli.add_command(curator)

if __name__ == '__main__':
    cli()
