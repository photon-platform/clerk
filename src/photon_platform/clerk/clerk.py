"""
clerk
"""
import os
from pathlib import Path

import click

from .progenitor.cli import progenitor
from .modulator.cli import modulator
from .curator.cli import curator
from .gather.cli import gather
from .logger.cli import logger
from .context import determine_context

@click.group()
@click.pass_context
def cli(ctx):
    """A command-line tool for situational awareness and context-sensitive operations."""
    ctx.ensure_object(dict)
    ctx.obj['context'] = determine_context(Path(os.getcwd()))

cli.add_command(progenitor)
cli.add_command(modulator)
cli.add_command(curator)
cli.add_command(gather)
cli.add_command(logger)

if __name__ == '__main__':
    cli()
