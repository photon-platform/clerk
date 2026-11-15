"""Context detection for Clerk across PHOTON and GEOMETOR workspaces."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "Context",
    "determine_context",
]


@dataclass
class Context:
    """Resolved filesystem, organization, and git context for a Clerk invocation."""

    path: Path
    org_name: str | None = None
    repo_name: str | None = None
    project_root: Path | None = None
    git_branch: str | None = None
    is_dirty: bool = False

    @property
    def is_project(self) -> bool:
        """Return whether ``path`` sits inside a detected repository root."""
        return self.project_root is not None

    @property
    def is_src(self) -> bool:
        """Return whether ``path`` is inside a ``src`` subtree."""
        return self.path.match("**/src*") or "src" in self.path.parts

    @property
    def is_docs(self) -> bool:
        """Return whether ``path`` is inside ``docs`` or ``docsrc``."""
        return any(self.path.match(f"**/{d}*") for d in ("docs", "docsrc")) or any(
            d in self.path.parts for d in ("docs", "docsrc")
        )

    @property
    def is_tests(self) -> bool:
        """Return whether ``path`` is inside a ``tests`` subtree."""
        return self.path.match("**/tests*") or "tests" in self.path.parts

    def export_for_agent(self) -> str:
        """Export the current context as a structured string for agents.

        Returns:
            Newline-delimited key/value summary of the detected context.
        """
        lines = [
            f"PATH: {self.path}",
            f"ORG: {self.org_name or 'N/A'}",
            f"REPO: {self.repo_name or 'N/A'}",
            f"BRANCH: {self.git_branch or 'N/A'}",
            f"DIRTY: {self.is_dirty}",
            f"TYPE: {'Project' if self.is_project else 'Generic'}",
        ]
        if self.is_src:
            lines.append("CONTEXT: Source Code")
        if self.is_docs:
            lines.append("CONTEXT: Documentation")
        if self.is_tests:
            lines.append("CONTEXT: Tests")

        return "\n".join(lines)


def determine_context(path: Path) -> Context:
    """Determine the workspace/repository context based on ``path``.

    Assumes a workspace hierarchy of ``~/PROJECTS/<org>/<repo>`` or git/pyproject
    markers. When ``path`` points directly to ``~/PROJECTS/<org>`` (even if an
    org-level ``pyproject.toml`` workspace manifest is present), ``org_name`` is
    resolved to ``<org>`` rather than misclassifying ``PROJECTS`` as an org.

    Args:
        path: Directory path to inspect.

    Returns:
        Populated :class:`Context` instance.
    """
    resolved = path.resolve()
    context = Context(path=resolved)

    current = resolved
    while current != current.parent:
        # Direct org-level directory (~/PROJECTS/<org>):
        if current.parent.name == "PROJECTS" and not (current / ".git").exists():
            context.org_name = current.name
            break

        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            context.project_root = current
            context.repo_name = current.name

            if (current / ".git").exists():
                try:
                    branch = (
                        subprocess.check_output(
                            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            cwd=current,
                            stderr=subprocess.DEVNULL,
                        )
                        .decode()
                        .strip()
                    )
                    context.git_branch = branch

                    status = (
                        subprocess.check_output(
                            ["git", "status", "--porcelain"],
                            cwd=current,
                            stderr=subprocess.DEVNULL,
                        )
                        .decode()
                        .strip()
                    )
                    context.is_dirty = bool(status)
                except (OSError, subprocess.SubprocessError):
                    context.git_branch = None

            projects_dir = current.parent.parent
            if projects_dir.name == "PROJECTS":
                context.org_name = current.parent.name
            elif current.parent.name == "PROJECTS":
                context.org_name = current.name
            break

        current = current.parent

    if not context.org_name:
        parts = resolved.parts
        if "PROJECTS" in parts:
            idx = parts.index("PROJECTS")
            if idx + 1 < len(parts):
                context.org_name = parts[idx + 1]

    return context
