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
from .context import determine_context

@click.group()
@click.pass_context
def cli(ctx):
    """A command-line tool for situational awareness and context-sensitive operations."""
    ctx.ensure_object(dict)
    ctx.obj['context'] = determine_context(Path(os.getcwd()))

cli.add_command(init)
cli.add_command(build)
cli.add_command(curate)
cli.add_command(gather)
cli.add_command(log)
cli.add_command(track)

if __name__ == '__main__':
    cli()
