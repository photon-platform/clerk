"""Canonical discovery and symlink management for PHOTON and GEOMETOR agent customizations."""

from __future__ import annotations

import errno
import os
import shutil
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

CustomizationKind = Literal["skill", "agent"]
ScopeName = Literal["all", "workspaces", "global"]
LinkStatus = Literal[
    "ok",
    "pending_source",
    "stale_copy",
    "wrong_target",
    "missing",
    "unmanaged",
]


@dataclass(frozen=True)
class ToolRepoSpec:
    """Specification for a repository hosting canonical skills and subagent definitions."""

    rel_path: str
    expected_skills: tuple[str, ...] = ()
    expected_agents: tuple[str, ...] = ()
    excluded_skills: frozenset[str] = frozenset()
    excluded_agents: frozenset[str] = frozenset()


DEFAULT_TOOL_REPO_SPECS: tuple[ToolRepoSpec, ...] = (
    ToolRepoSpec(
        rel_path="photon-platform/clerk",
        expected_skills=("clerk-branch", "clerk-rollup"),
        expected_agents=("clerk.md",),
    ),
    ToolRepoSpec(
        rel_path="photon-platform/publish",
        expected_skills=("scriptorium-codex",),
        expected_agents=("scriptorium.md",),
    ),
    ToolRepoSpec(
        rel_path="geometor/.config",
        expected_skills=("geometor-construct",),
        expected_agents=("geometer.md",),
    ),
    ToolRepoSpec(
        rel_path="photon-platform/studio",
        expected_skills=("studio",),
        expected_agents=("studio.md",),
        excluded_skills=frozenset(
            {
                "clerk-branch",
                "clerk-rollup",
                "dialogue",
                "euclid-shorts",
                "podcaster",
                "presenter",
                "producer",
                "shorts",
            }
        ),
        excluded_agents=frozenset(
            {
                "dialogue.md",
                "euclid-shorts.md",
                "podcaster.md",
                "presenter.md",
                "producer.md",
                "shorts.md",
            }
        ),
    ),
)

DEFAULT_WORKSPACE_NAMES: tuple[str, ...] = ("geometor", "photon-platform")


@dataclass(frozen=True)
class CustomizationItem:
    """A canonical skill directory or subagent Markdown definition."""

    kind: CustomizationKind
    name: str
    repo: str
    source_path: Path
    source_exists: bool

    def to_dict(self) -> dict[str, Any]:
        """Serialize item to a JSON-friendly dictionary."""
        data = asdict(self)
        data["source_path"] = str(self.source_path)
        return data


@dataclass(frozen=True)
class TargetRoot:
    """A destination customization root (`.agents/` in a workspace or `~/.gemini/config`)."""

    label: str
    scope: Literal["workspaces", "global"]
    root_path: Path

    def link_dir(self, kind: CustomizationKind) -> Path:
        """Return the `skills/` or `agents/` subdirectory inside this target root."""
        return self.root_path / ("skills" if kind == "skill" else "agents")


@dataclass(frozen=True)
class LinkCheck:
    """Verification result for a single customization entry inside a target root."""

    target_label: str
    kind: CustomizationKind
    name: str
    repo: str
    link_path: Path
    source_path: Path | None
    status: LinkStatus
    detail: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize check to a JSON-friendly dictionary."""
        return {
            "target_label": self.target_label,
            "kind": self.kind,
            "name": self.name,
            "repo": self.repo,
            "link_path": str(self.link_path),
            "source_path": str(self.source_path) if self.source_path else None,
            "status": self.status,
            "detail": self.detail,
        }


@dataclass
class StatusReport:
    """Aggregate report returned by `check_status`."""

    projects_dir: Path
    scope: ScopeName
    canonical_items: list[CustomizationItem] = field(default_factory=list)
    checks: list[LinkCheck] = field(default_factory=list)
    collisions: list[str] = field(default_factory=list)

    @property
    def managed_checks(self) -> list[LinkCheck]:
        """Return checks corresponding to canonical managed items."""
        return [c for c in self.checks if c.status != "unmanaged"]

    @property
    def unmanaged_checks(self) -> list[LinkCheck]:
        """Return checks corresponding to unmanaged stray entries."""
        return [c for c in self.checks if c.status == "unmanaged"]

    @property
    def all_ok(self) -> bool:
        """Return True if all canonical sources exist and all managed links are `ok`."""
        return (
            all(item.source_exists for item in self.canonical_items)
            and all(c.status == "ok" for c in self.managed_checks)
            and not self.collisions
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize full report to a JSON-friendly dictionary."""
        counts: dict[str, int] = {}
        for check in self.checks:
            counts[check.status] = counts.get(check.status, 0) + 1
        return {
            "projects_dir": str(self.projects_dir),
            "scope": self.scope,
            "all_ok": self.all_ok,
            "counts": counts,
            "collisions": list(self.collisions),
            "canonical_items": [item.to_dict() for item in self.canonical_items],
            "checks": [check.to_dict() for check in self.checks],
        }


@dataclass(frozen=True)
class SyncAction:
    """Result of synchronizing a single customization link."""

    target_label: str
    kind: CustomizationKind
    name: str
    link_path: Path
    source_path: Path | None
    action: str
    detail: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize sync action to a JSON-friendly dictionary."""
        return {
            "target_label": self.target_label,
            "kind": self.kind,
            "name": self.name,
            "link_path": str(self.link_path),
            "source_path": str(self.source_path) if self.source_path else None,
            "action": self.action,
            "detail": self.detail,
        }


@dataclass
class SyncReport:
    """Aggregate report returned by `sync_links`."""

    dry_run: bool
    scope: ScopeName
    actions: list[SyncAction] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """Return True if no errors occurred during synchronization."""
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        """Serialize sync report to a JSON-friendly dictionary."""
        counts: dict[str, int] = {}
        for act in self.actions:
            counts[act.action] = counts.get(act.action, 0) + 1
        return {
            "dry_run": self.dry_run,
            "scope": self.scope,
            "ok": self.ok,
            "counts": counts,
            "errors": list(self.errors),
            "actions": [act.to_dict() for act in self.actions],
        }


def default_projects_dir() -> Path:
    """Return the default PROJECTS directory (`~/PROJECTS`)."""
    return Path.home() / "PROJECTS"


def default_global_config_dir() -> Path:
    """Return the default global Antigravity config directory (`~/.gemini/config`)."""
    return Path.home() / ".gemini" / "config"


def _skill_exists(skill_dir: Path) -> bool:
    return skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file()


def discover_customizations(
    projects_dir: Path | None = None,
    specs: Sequence[ToolRepoSpec] = DEFAULT_TOOL_REPO_SPECS,
) -> tuple[list[CustomizationItem], list[str]]:
    """Discover canonical skills and subagent definitions across configured tool repos.

    Args:
        projects_dir: Base `PROJECTS` root containing `<org>/<repo>` folders.
        specs: Ordered sequence of tool repository specifications.

    Returns:
        A tuple `(items, collisions)` of deduplicated `CustomizationItem` records and
        collision warning messages.
    """
    base_dir = (projects_dir or default_projects_dir()).resolve(strict=False)
    seen: dict[tuple[CustomizationKind, str], str] = {}
    items: list[CustomizationItem] = []
    collisions: list[str] = []

    def _register(kind: CustomizationKind, name: str, repo: str, src: Path, exists: bool) -> None:
        key = (kind, name)
        if key in seen:
            if seen[key] != repo:
                collisions.append(
                    f"Duplicate {kind} '{name}' in {repo} ignored (canonical owner: {seen[key]})"
                )
            return
        seen[key] = repo
        items.append(
            CustomizationItem(
                kind=kind,
                name=name,
                repo=repo,
                source_path=src,
                source_exists=exists,
            )
        )

    for spec in specs:
        repo_root = base_dir / spec.rel_path
        skills_dir = repo_root / "skills"
        agents_dir = repo_root / "agents"

        for skill_name in spec.expected_skills:
            if skill_name in spec.excluded_skills:
                continue
            src = (skills_dir / skill_name).resolve(strict=False)
            _register("skill", skill_name, spec.rel_path, src, _skill_exists(src))

        if skills_dir.is_dir():
            for child in sorted(skills_dir.iterdir(), key=lambda p: p.name):
                if child.name.startswith((".", "_")) or child.name in spec.excluded_skills:
                    continue
                if _skill_exists(child):
                    _register(
                        "skill",
                        child.name,
                        spec.rel_path,
                        child.resolve(strict=False),
                        True,
                    )

        for agent_name in spec.expected_agents:
            if agent_name in spec.excluded_agents:
                continue
            src = (agents_dir / agent_name).resolve(strict=False)
            _register("agent", agent_name, spec.rel_path, src, src.is_file())

        if agents_dir.is_dir():
            for child in sorted(agents_dir.glob("*.md"), key=lambda p: p.name):
                if child.name.startswith((".", "_")) or child.name in spec.excluded_agents:
                    continue
                if child.is_file():
                    _register(
                        "agent",
                        child.name,
                        spec.rel_path,
                        child.resolve(strict=False),
                        True,
                    )

    return items, collisions


def build_target_roots(
    projects_dir: Path | None = None,
    global_config_dir: Path | None = None,
    scope: ScopeName = "all",
    workspace_names: Sequence[str] = DEFAULT_WORKSPACE_NAMES,
) -> list[TargetRoot]:
    """Build the ordered list of target customization roots for the requested scope."""
    base_dir = (projects_dir or default_projects_dir()).resolve(strict=False)
    global_dir = (global_config_dir or default_global_config_dir()).resolve(strict=False)

    roots: list[TargetRoot] = []
    if scope in ("all", "workspaces"):
        for ws in workspace_names:
            roots.append(
                TargetRoot(
                    label=f"workspace:{ws}",
                    scope="workspaces",
                    root_path=base_dir / ws / ".agents",
                )
            )
    if scope in ("all", "global"):
        roots.append(
            TargetRoot(
                label="global:gemini-config",
                scope="global",
                root_path=global_dir,
            )
        )
    return roots


def _resolve_symlink_target(link_path: Path) -> Path:
    raw_target = Path(os.readlink(link_path))
    if not raw_target.is_absolute():
        raw_target = link_path.parent / raw_target
    return raw_target.resolve(strict=False)


def inspect_link(target: TargetRoot, item: CustomizationItem) -> LinkCheck:
    """Inspect a single canonical item's symlink state inside a target root."""
    link_path = target.link_dir(item.kind) / item.name
    expected_target = item.source_path.resolve(strict=False)

    if link_path.is_symlink():
        actual_target = _resolve_symlink_target(link_path)
        if actual_target == expected_target:
            if item.source_exists:
                return LinkCheck(
                    target_label=target.label,
                    kind=item.kind,
                    name=item.name,
                    repo=item.repo,
                    link_path=link_path,
                    source_path=item.source_path,
                    status="ok",
                    detail=f"-> {actual_target}",
                )
            return LinkCheck(
                target_label=target.label,
                kind=item.kind,
                name=item.name,
                repo=item.repo,
                link_path=link_path,
                source_path=item.source_path,
                status="pending_source",
                detail=f"symlink ready -> {actual_target} (canonical file not yet created)",
            )
        return LinkCheck(
            target_label=target.label,
            kind=item.kind,
            name=item.name,
            repo=item.repo,
            link_path=link_path,
            source_path=item.source_path,
            status="wrong_target",
            detail=f"points to {actual_target} (expected {expected_target})",
        )

    if link_path.exists():
        kind_desc = "directory" if link_path.is_dir() else "file"
        return LinkCheck(
            target_label=target.label,
            kind=item.kind,
            name=item.name,
            repo=item.repo,
            link_path=link_path,
            source_path=item.source_path,
            status="stale_copy",
            detail=f"disconnected {kind_desc} copy (expected symlink -> {expected_target})",
        )

    return LinkCheck(
        target_label=target.label,
        kind=item.kind,
        name=item.name,
        repo=item.repo,
        link_path=link_path,
        source_path=item.source_path,
        status="missing",
        detail=f"not linked (expected -> {expected_target})",
    )


def check_status(
    projects_dir: Path | None = None,
    global_config_dir: Path | None = None,
    scope: ScopeName = "all",
    specs: Sequence[ToolRepoSpec] = DEFAULT_TOOL_REPO_SPECS,
    workspace_names: Sequence[str] = DEFAULT_WORKSPACE_NAMES,
) -> StatusReport:
    """Check canonical customization sources and symlink alignment across targets."""
    base_dir = (projects_dir or default_projects_dir()).resolve(strict=False)
    items, collisions = discover_customizations(projects_dir=base_dir, specs=specs)
    targets = build_target_roots(
        projects_dir=base_dir,
        global_config_dir=global_config_dir,
        scope=scope,
        workspace_names=workspace_names,
    )

    managed_by_kind: dict[CustomizationKind, set[str]] = {
        "skill": {i.name for i in items if i.kind == "skill"},
        "agent": {i.name for i in items if i.kind == "agent"},
    }

    checks: list[LinkCheck] = []
    for target in targets:
        for item in items:
            checks.append(inspect_link(target, item))

        for kind in ("skill", "agent"):
            subdir = target.link_dir(kind)
            if not subdir.is_dir():
                continue
            for entry in sorted(subdir.iterdir(), key=lambda p: p.name):
                if entry.name.startswith("."):
                    continue
                if entry.name not in managed_by_kind[kind]:
                    detail = (
                        f"unmanaged symlink -> {_resolve_symlink_target(entry)}"
                        if entry.is_symlink()
                        else "unmanaged local entry"
                    )
                    checks.append(
                        LinkCheck(
                            target_label=target.label,
                            kind=kind,
                            name=entry.name,
                            repo="unmanaged",
                            link_path=entry,
                            source_path=None,
                            status="unmanaged",
                            detail=detail,
                        )
                    )

    return StatusReport(
        projects_dir=base_dir,
        scope=scope,
        canonical_items=items,
        checks=checks,
        collisions=collisions,
    )


def _remove_existing_entry(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _is_readonly_oserror(exc: OSError) -> bool:
    return exc.errno in (errno.EROFS, errno.EACCES, errno.EPERM)


def sync_links(
    projects_dir: Path | None = None,
    global_config_dir: Path | None = None,
    scope: ScopeName = "all",
    dry_run: bool = False,
    replace_copies: bool = True,
    prune_unmanaged: bool = False,
    link_pending: bool = True,
    specs: Sequence[ToolRepoSpec] = DEFAULT_TOOL_REPO_SPECS,
    workspace_names: Sequence[str] = DEFAULT_WORKSPACE_NAMES,
) -> SyncReport:
    """Create or repair symlinks in workspace `.agents/` and `~/.gemini/config/`.

    Args:
        projects_dir: Base `PROJECTS` root directory.
        global_config_dir: Global Antigravity config directory (`~/.gemini/config`).
        scope: Which targets to synchronize (`"all"`, `"workspaces"`, or `"global"`).
        dry_run: If True, report planned mutations without modifying the filesystem.
        replace_copies: If True, replace stale file/directory copies with symlinks.
        prune_unmanaged: If True, remove unmanaged entries in target directories.
        link_pending: If True, create symlinks even when a declared canonical file is pending.
        specs: Tool repository specifications.
        workspace_names: Workspace folder names under `projects_dir`.

    Returns:
        A `SyncReport` summarizing all actions and any filesystem errors.
    """
    base_dir = (projects_dir or default_projects_dir()).resolve(strict=False)
    items, _ = discover_customizations(projects_dir=base_dir, specs=specs)
    targets = build_target_roots(
        projects_dir=base_dir,
        global_config_dir=global_config_dir,
        scope=scope,
        workspace_names=workspace_names,
    )

    managed_by_kind: dict[CustomizationKind, set[str]] = {
        "skill": {i.name for i in items if i.kind == "skill"},
        "agent": {i.name for i in items if i.kind == "agent"},
    }

    report = SyncReport(dry_run=dry_run, scope=scope)

    for target in targets:
        for item in items:
            check = inspect_link(target, item)
            if not item.source_exists and not link_pending:
                report.actions.append(
                    SyncAction(
                        target_label=target.label,
                        kind=item.kind,
                        name=item.name,
                        link_path=check.link_path,
                        source_path=item.source_path,
                        action="skipped_missing_source",
                        detail=f"canonical source missing: {item.source_path}",
                    )
                )
                continue

            if check.status in ("ok", "pending_source"):
                report.actions.append(
                    SyncAction(
                        target_label=target.label,
                        kind=item.kind,
                        name=item.name,
                        link_path=check.link_path,
                        source_path=item.source_path,
                        action="unchanged",
                        detail=check.detail,
                    )
                )
                continue

            if check.status == "stale_copy" and not replace_copies:
                report.actions.append(
                    SyncAction(
                        target_label=target.label,
                        kind=item.kind,
                        name=item.name,
                        link_path=check.link_path,
                        source_path=item.source_path,
                        action="skipped_stale_copy",
                        detail=check.detail,
                    )
                )
                continue

            planned_verb = (
                "replaced_copy"
                if check.status == "stale_copy"
                else "retargeted"
                if check.status == "wrong_target"
                else "linked"
            )
            if dry_run:
                report.actions.append(
                    SyncAction(
                        target_label=target.label,
                        kind=item.kind,
                        name=item.name,
                        link_path=check.link_path,
                        source_path=item.source_path,
                        action=f"would_{planned_verb}",
                        detail=f"{check.link_path} -> {item.source_path}",
                    )
                )
                continue

            try:
                check.link_path.parent.mkdir(parents=True, exist_ok=True)
                if check.link_path.is_symlink() or check.link_path.exists():
                    _remove_existing_entry(check.link_path)
                check.link_path.symlink_to(item.source_path)
                report.actions.append(
                    SyncAction(
                        target_label=target.label,
                        kind=item.kind,
                        name=item.name,
                        link_path=check.link_path,
                        source_path=item.source_path,
                        action=planned_verb,
                        detail=f"-> {item.source_path}",
                    )
                )
            except OSError as exc:
                action_name = "skipped_readonly" if _is_readonly_oserror(exc) else "error"
                msg = f"{target.label} ({check.link_path}): {exc}"
                report.errors.append(msg)
                report.actions.append(
                    SyncAction(
                        target_label=target.label,
                        kind=item.kind,
                        name=item.name,
                        link_path=check.link_path,
                        source_path=item.source_path,
                        action=action_name,
                        detail=str(exc),
                    )
                )

        if prune_unmanaged:
            for kind in ("skill", "agent"):
                subdir = target.link_dir(kind)
                if not subdir.is_dir():
                    continue
                for entry in sorted(subdir.iterdir(), key=lambda p: p.name):
                    if entry.name.startswith(".") or entry.name in managed_by_kind[kind]:
                        continue
                    if dry_run:
                        report.actions.append(
                            SyncAction(
                                target_label=target.label,
                                kind=kind,
                                name=entry.name,
                                link_path=entry,
                                source_path=None,
                                action="would_prune",
                                detail="unmanaged entry",
                            )
                        )
                        continue
                    try:
                        _remove_existing_entry(entry)
                        report.actions.append(
                            SyncAction(
                                target_label=target.label,
                                kind=kind,
                                name=entry.name,
                                link_path=entry,
                                source_path=None,
                                action="pruned",
                                detail="removed unmanaged entry",
                            )
                        )
                    except OSError as exc:
                        msg = f"{target.label} prune ({entry}): {exc}"
                        report.errors.append(msg)

    return report
