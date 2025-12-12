import click
import os
from . import curator as curator_actions
from . import rollup as rollup_module
from . import status_diff as status_diff_module

@click.group()
def curate():
    """Organizes git/archive management."""
    pass

@curate.command('branches')
@click.option('--repo-path', default='', help='The path to the repository.')
@click.pass_context
def branches(ctx, repo_path):
    """Lists the branches in the repository."""
    context = ctx.obj.get('context')
    path = repo_path
    if not path and context and context.is_project:
        path = str(context.project_root)
    elif not path:
        path = '.'

    repo = curator_actions.action_get_repo(path)
    branches = curator_actions.action_get_branches(repo)
    for branch, is_active in branches.items():
        if is_active:
            click.echo(f"* {branch}")
        else:
            click.echo(f"  {branch}")

@curate.command('create-release-branch')
@click.option('--repo-path', default='', help='The path to the repository.')
@click.option('--release-version', prompt='Release Version', help='The version number for the release.')
@click.option('--description', prompt='Description', help='A short description of the release.')
@click.pass_context
def create_release_branch(ctx, repo_path, release_version, description):
    """Creates a new release branch."""
    context = ctx.obj.get('context')
    path = repo_path
    if not path and context and context.is_project:
        path = str(context.project_root)
    elif not path:
        path = '.'

    repo = curator_actions.action_get_repo(path)
    success, message = curator_actions.action_create_release_branch(repo, release_version, description)
    if success:
        click.echo(message)
    else:
        click.echo(f"Error: {message}")

@curate.command('merge-to-main')
@click.option('--repo-path', default='', help='The path to the repository.')
@click.option('--branch-name', prompt='Branch Name', help='The name of the branch to merge.')
@click.option('--commit-message', prompt='Commit Message', help='The commit message.')
@click.pass_context
def merge_to_main(ctx, repo_path, branch_name, commit_message):
    """Merges a branch to main."""
    context = ctx.obj.get('context')
    path = repo_path
    if not path and context and context.is_project:
        path = str(context.project_root)
    elif not path:
        path = '.'

    repo = curator_actions.action_get_repo(path)
    success, message = curator_actions.action_merge_to_main(repo, branch_name, commit_message)
    if success:
        click.echo(message)
    else:
        click.echo(f"Error: {message}")

@curate.command('create-tag')
@click.option('--repo-path', default='', help='The path to the repository.')
@click.option('--tag-name', prompt='Tag Name', help='The name of the tag.')
@click.option('--message', prompt='Message', help='The message for the tag.')
@click.pass_context
def create_tag(ctx, repo_path, tag_name, message):
    """Creates a new tag."""
    context = ctx.obj.get('context')
    path = repo_path
    if not path and context and context.is_project:
        path = str(context.project_root)
    elif not path:
        path = '.'

    repo = curator_actions.action_get_repo(path)
    success, message = curator_actions.action_create_tag(repo, tag_name, message)
    if success:
        click.echo(message)
    else:
        click.echo(f"Error: {message}")

@curate.command('init')
def init_repo():
    """Initializes a new git repository."""
    from . import git_init
    git_init.main()

@curate.command('rollup')
def rollup():
    """Automates the release process."""
    rollup_module.rollup()

@curate.command('status')
def status():
    """Shows git status and diff."""
    status_diff_module.status_diff()
