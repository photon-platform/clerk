"""CLI command for initializing new PHOTON and GEOMETOR repositories."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import click

from .progenitor import ARCHETYPES, create_project

__all__ = ["init"]


@click.command()
@click.argument("project_name")
@click.option("--description", "-d", default=None, help="Short repository summary.")
@click.option(
    "--type",
    "-t",
    "archetype",
    type=click.Choice(list(ARCHETYPES), case_sensitive=False),
    default="code",
    show_default=True,
    help="Repository archetype: code package, historical codex, or mathematical catalog.",
)
@click.option(
    "--edition",
    "edition_slug",
    default=None,
    help="Primary edition directory slug for --type codex (defaults to sanitized project name).",
)
@click.option(
    "--title",
    "book_title",
    default=None,
    help="Display title for a codex treatise or mathematical catalog.",
)
@click.option(
    "--book-author",
    "book_author",
    default=None,
    help="Historical or primary source author attribution for codex/catalog projects.",
)
@click.option(
    "--org",
    "org_override",
    default=None,
    help="Override detected GitHub organization slug (e.g. geometor, photon-platform).",
)
@click.option(
    "--git/--no-git",
    "git_init",
    default=True,
    show_default=True,
    help="Initialize a git repository on branch main.",
)
@click.pass_context
def init(
    ctx: click.Context,
    project_name: str,
    description: str | None,
    archetype: str,
    edition_slug: str | None,
    book_title: str | None,
    book_author: str | None,
    org_override: str | None,
    git_init: bool,
) -> None:
    """Create a new Python 3.13 project, codex, or mathematical catalog."""
    context = ctx.obj.get("context") if ctx.obj else None
    github_id = org_override or (context.org_name if context else None)

    if not github_id:
        click.echo(
            "Could not detect Organization context. "
            "Please ensure you are in ~/PROJECTS/<org> or pass --org <org>."
        )
        return

    package_namespace = github_id.replace("-", "_")
    package_name = project_name.replace("-", "_").replace(" ", "_")
    target_parent = Path(os.getcwd())

    try:
        author = (
            subprocess.check_output(["git", "config", "user.name"], stderr=subprocess.DEVNULL)
            .decode("utf-8")
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        author = ""
    if not author:
        author = "phi ARCHITECT"

    created = create_project(
        github_id=github_id,
        package_namespace=package_namespace,
        github_repo_id=project_name,
        package_name=package_name,
        author=author,
        description=description,
        path=target_parent,
        archetype=archetype,
        edition_slug=edition_slug,
        book_title=book_title,
        book_author=book_author,
        git_init=git_init,
    )
    if created is not None:
        click.echo(
            f"Initialized {archetype} repository '{github_id}/{project_name}' at {created}"
        )
