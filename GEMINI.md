# CLERK

A command-line tool for situational awareness, repository curation, and agent customization management across the PHOTON and GEOMETOR ecosystems.

## Overview

CLERK (Command-Line Executor for Rapid Knowledge) provides context-sensitive operations based on the current working directory and repository lineage (`~/PROJECTS/<org>/<repo>`). It also serves as the canonical home of the `clerk-branch` and `clerk-rollup` workflow skills and the `clerk` release-curation subagent.

## Integrated Tools

- **`agents`**: Discovers canonical `skills/*` and `agents/*.md` across PHOTON/GEOMETOR tool repos (`photon-platform/clerk`, `photon-platform/publish`, `geometor/.config`, `photon-platform/studio`) and verifies/synchronizes symlinks into workspace `.agents/` and `~/.gemini/config/` (`clerk agents status`, `clerk agents sync`).
- **`init`**: Scaffolds new Python namespace-package projects.
- **`build`**: Shapes Python modules and packages.
- **`curate`**: Organizes git branch, release, and archive management.
- **`log`**: Creates journal-day documentation log entries (`docsrc/log/`).
- **`track`**: Scans for and reports on project tasks/todos.
- **`gather`**: Gathers and summarizes external research content.
- **`navigator`**: TUI Miller-column browser for organizations and repositories.

## Canonical Agent Customizations (`skills/` & `agents/`)

- `skills/clerk-branch/SKILL.md`: Multi-repo feature/fix branching, boundary verification, Python 3.13 `uv --no-sync` baseline checks, and implementation planning.
- `skills/clerk-rollup/SKILL.md`: Branch verification (`pytest`, `ruff check`, `publish build`), `CHANGELOG.rst` + `__version__` + `docsrc/log/` curation, merge to `main`, tagging, and pushing.
- `agents/clerk.md`: Subagent persona for repository hygiene, quality gates, and release rollups.
