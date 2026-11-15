"""CLI command for creating Sphinx log entries."""

from __future__ import annotations

import click

from .logger import create_log_entry

__all__ = ["log"]


@click.command()
@click.option("--title", prompt="Title", help="Title for log entry.")
@click.option("--excerpt", prompt="Excerpt", default="", help="Short description.")
@click.option("--tags", prompt="Tags", default="", help="Comma-separated list of tags.")
@click.option(
    "--category",
    prompt="Category",
    default="",
    help="Comma-separated list of categories.",
)
@click.option("--image", prompt="Image", default="", help="Path to image.")
@click.option("--author", default="phi ARCHITECT", show_default=True, help="Log entry author.")
@click.pass_context
def log(
    ctx: click.Context,
    title: str,
    excerpt: str,
    tags: str,
    category: str,
    image: str,
    author: str,
) -> None:
    """Create a new chronological log entry under ``docsrc/log/``."""
    context = ctx.obj.get("context") if ctx.obj else None

    if not context or not context.is_project or context.project_root is None:
        click.echo("Logger must be run within a project context.")
        return

    filename = create_log_entry(
        context.project_root,
        title=title,
        excerpt=excerpt,
        tags=tags,
        category=category,
        image=image,
        author=author,
    )
    click.echo(f"Log entry created at: {filename}")
