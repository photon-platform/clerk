import click
from . import gather as gather_actions

@click.group()
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
