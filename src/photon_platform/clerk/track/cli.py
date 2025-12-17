"""Clerk track CLI module."""
import click
import os
from pathlib import Path
from .core import get_todos, report_todos_md, report_todos_rich, report_todos_json, report_todos_list

@click.group(invoke_without_command=True)
@click.option('--group', is_flag=True, help='Group output by project')
@click.pass_context
def track(ctx: click.Context, group: bool) -> None:
    """Scan for todo files and generate a status report."""
    if ctx.invoked_subcommand is None:
        cwd = Path(os.getcwd())
        todos = get_todos(cwd)
        report_todos_rich(todos, group_by_project=group)

@track.command()
def md() -> None:
    """Output report in Markdown format."""
    cwd = Path(os.getcwd())
    todos = get_todos(cwd)
    report_todos_md(todos)

@track.command()
def json() -> None:
    """Output report in JSON format."""
    cwd = Path(os.getcwd())
    todos = get_todos(cwd)
    report_todos_json(todos)

@track.command(name="list")
def list_titles() -> None:
    """Output simple list of todo titles."""
    cwd = Path(os.getcwd())
    todos = get_todos(cwd)
    report_todos_list(todos)

