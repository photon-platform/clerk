"""Click CLI commands for `clerk agents` (`status` and `sync`)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import click
from rich.console import Console
from rich.table import Table

from .registry import ScopeName, check_status, sync_links

_STATUS_STYLE: dict[str, str] = {
    "ok": "green",
    "pending_source": "yellow",
    "stale_copy": "bold red",
    "wrong_target": "bold red",
    "missing": "yellow",
    "unmanaged": "cyan",
}


@click.group("agents")
def agents() -> None:
    """Manage canonical agent definitions, skills, and workspace/global symlinks."""


@agents.command("status")
@click.option(
    "--scope",
    type=click.Choice(["all", "workspaces", "global"], case_sensitive=False),
    default="all",
    show_default=True,
    help="Target customization roots to inspect.",
)
@click.option(
    "--projects-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Override base PROJECTS directory (defaults to ~/PROJECTS).",
)
@click.option(
    "--global-config-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Override global config directory (defaults to ~/.gemini/config).",
)
@click.option("--json", "as_json", is_flag=True, help="Emit structured JSON report.")
@click.option(
    "--strict",
    is_flag=True,
    help="Exit with non-zero status if any managed customization is drifted or missing.",
)
def status_cmd(
    scope: str,
    projects_dir: Path | None,
    global_config_dir: Path | None,
    as_json: bool,
    strict: bool,
) -> None:
    """Inspect canonical skills and subagent symlinks across workspaces and global config."""
    report = check_status(
        projects_dir=projects_dir,
        global_config_dir=global_config_dir,
        scope=cast(ScopeName, scope.lower()),
    )

    if as_json:
        click.echo(json.dumps(report.to_dict(), indent=2))
    else:
        console = Console()

        src_table = Table(title="Canonical Agent Customizations")
        src_table.add_column("Kind", style="bold")
        src_table.add_column("Name")
        src_table.add_column("Owner Repo")
        src_table.add_column("Source Status")
        for item in report.canonical_items:
            src_status = (
                "[green]present[/green]" if item.source_exists else "[yellow]missing[/yellow]"
            )
            src_table.add_row(item.kind, item.name, item.repo, src_status)
        console.print(src_table)

        link_table = Table(title=f"Symlink Alignment ({report.scope})")
        link_table.add_column("Target", style="bold")
        link_table.add_column("Kind")
        link_table.add_column("Name")
        link_table.add_column("Status")
        link_table.add_column("Detail")
        for chk in report.checks:
            style = _STATUS_STYLE.get(chk.status, "white")
            link_table.add_row(
                chk.target_label,
                chk.kind,
                chk.name,
                f"[{style}]{chk.status}[/{style}]",
                chk.detail,
            )
        console.print(link_table)

        for warning in report.collisions:
            console.print(f"[yellow]Warning:[/yellow] {warning}")

    if strict and not report.all_ok:
        raise SystemExit(1)


@agents.command("sync")
@click.option(
    "--scope",
    type=click.Choice(["all", "workspaces", "global"], case_sensitive=False),
    default="all",
    show_default=True,
    help="Target customization roots to synchronize.",
)
@click.option(
    "--projects-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Override base PROJECTS directory (defaults to ~/PROJECTS).",
)
@click.option(
    "--global-config-dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Override global config directory (defaults to ~/.gemini/config).",
)
@click.option("--dry-run", is_flag=True, help="Preview symlink updates without writing.")
@click.option(
    "--keep-copies",
    is_flag=True,
    help="Do not replace disconnected file/directory copies with symlinks.",
)
@click.option(
    "--prune",
    is_flag=True,
    help="Remove unmanaged entries inside target skills/ and agents/ folders.",
)
@click.option("--json", "as_json", is_flag=True, help="Emit structured JSON report.")
def sync_cmd(
    scope: str,
    projects_dir: Path | None,
    global_config_dir: Path | None,
    dry_run: bool,
    keep_copies: bool,
    prune: bool,
    as_json: bool,
) -> None:
    """Synchronize workspace `.agents/` and `~/.gemini/config/` symlinks to git repos."""
    report = sync_links(
        projects_dir=projects_dir,
        global_config_dir=global_config_dir,
        scope=cast(ScopeName, scope.lower()),
        dry_run=dry_run,
        replace_copies=not keep_copies,
        prune_unmanaged=prune,
    )

    if as_json:
        click.echo(json.dumps(report.to_dict(), indent=2))
    else:
        console = Console()
        title = "Agent Symlink Sync (DRY RUN)" if dry_run else "Agent Symlink Sync"
        table = Table(title=title)
        table.add_column("Target", style="bold")
        table.add_column("Kind")
        table.add_column("Name")
        table.add_column("Action")
        table.add_column("Detail")
        for act in report.actions:
            color = (
                "green"
                if act.action in ("linked", "replaced_copy", "retargeted", "unchanged")
                else "yellow"
                if act.action.startswith(("would_", "skipped_"))
                else "red"
            )
            table.add_row(
                act.target_label,
                act.kind,
                act.name,
                f"[{color}]{act.action}[/{color}]",
                act.detail,
            )
        console.print(table)

        if report.errors:
            console.print(
                "[yellow]Note:[/yellow] Some targets were not writable in this environment "
                "(for example, `~/.gemini/config` inside a read-only sandbox). "
                "Run `clerk agents sync --scope global` on the host to update `~/.gemini/config`."
            )

    if not report.ok:
        raise SystemExit(1)
