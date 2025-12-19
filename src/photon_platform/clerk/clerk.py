"""
clerk
"""
import os
from pathlib import Path

import click

from .init.cli import init
from .build.cli import build
from .curate.cli import curate
from .gather.cli import gather
from .log.cli import log
from .track.cli import track
from .context import determine_context, Context

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A command-line tool for situational awareness and context-sensitive operations."""
    ctx.ensure_object(dict)
    context = determine_context(Path(os.getcwd()))
    ctx.obj['context'] = context

    if ctx.invoked_subcommand is None:
        from .navigator.app import ClerkNavigator
        app = ClerkNavigator(context)
        app.run()

@cli.command()
@click.argument("path", default=".", type=click.Path(exists=True))
def navigator(path: str) -> None:
    """Launch the Clerk Navigator TUI."""
    from .navigator.app import ClerkNavigator
    # Ensure we use determine_context to get a proper Context object
    context = determine_context(Path(path).resolve())
    app = ClerkNavigator(context)
    exit_path = app.run()
    if exit_path:
        print(exit_path)

cli.add_command(init)
cli.add_command(build)
cli.add_command(curate)
cli.add_command(gather)
cli.add_command(log)
cli.add_command(track)
cli.add_command(navigator)

if __name__ == '__main__':
    cli()
