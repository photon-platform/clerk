---
name: clerk-branch
description: >-
  Start a coordinated git feature or fix branch across affected PHOTON and GEOMETOR
  repositories, verify baseline tests and repository boundaries, refine scope, and
  produce an explicit implementation plan before modifying code.
---

# Clerk Branch Workflow (`clerk-branch`)

Use this runbook whenever starting a new feature, refactor, or bug-fix task across one or more repositories in `/home/phi/PROJECTS/{photon-platform,geometor,phiarchitect,harmonic-resonance}`.

---

## 1. Audit Repository State & Declare Boundaries

Before creating branches or editing files, inspect every target repository and confirm there are no uncommitted conflicts or parallel-agent boundary overlaps:

1. **Prefix-Matchable Git Inspection** (never use `cd`, `&&`, `;`, `||`, `$(...)`, `env`, or `bash -c`):
   ```bash
   git -C /home/phi/PROJECTS/<org>/<repo> status
   git -C /home/phi/PROJECTS/<org>/<repo> branch --show-current
   ```
2. **Multi-Repo Coordination**:
   - Identify *all* repositories touched by the task (for example, `photon-platform/publish` + `geometor/euclid`, or `geometor/model` + `geometor/elements`).
   - Use the **same branch slug** across coupled repositories when shipping a coordinated cross-repo change (e.g., `feature/<slug>` or `fix/<slug>`).
   - Explicitly list **out-of-bounds** repositories when running alongside parallel subagents so zero working-tree collisions occur.

---

## 2. Create Feature or Fix Branches

1. Ensure you are branching from an up-to-date `main` (unless intentionally stacking on a specified parent branch):
   ```bash
   git -C /home/phi/PROJECTS/<org>/<repo> switch main
   ```
   *(Only run `git -C ... pull origin main` with `BypassSandbox: true` if remote sync was requested or needed.)*
2. Create and switch to the new branch in each affected repository:
   ```bash
   git -C /home/phi/PROJECTS/<org>/<repo> switch -c feature/<short-kebab-slug>
   ```
   Use `feature/<slug>` for new capabilities/content and `fix/<slug>` for bug fixes or regressions.

---

## 3. Refine Scope & Verify Baseline

1. **Read Repository Context**:
   - Read `GEMINI.md`, `README.rst`, `STANDARDS.md`, and `ROADMAP.md` (if present) in each target repository.
   - Check `src/<namespace>/<repo_name>/__init__.py` for the current `__version__` and public exports.
2. **Verify Python 3.13 Sandbox Baseline**:
   - All commands run via `uv`-managed Python 3.13 inside the offline terminal sandbox (`--no-sync` prevents PyPI network calls):
     ```bash
     uv run --no-sync pytest
     ruff check src tests
     ```
   - Clarify any ambiguous user requirements before writing implementation code.

---

## 4. Implementation Plan

Outline a concise, verifiable plan before applying edits:

1. **Target Files & Modules**: Exact paths under `src/<namespace>/<repo_name>/`, `docsrc/`, `skills/`, or `agents/` to create or modify.
2. **Invariants & Standards**:
   - `from __future__ import annotations` + strict Python 3.13 type annotations (`list[...]`, `dict[...]`, `X | None`) + Google-style docstrings.
   - Domain rules (e.g., 100% exact SymPy algebra in `geometor`, zero embedded `py_file` scripts in historical codices, real git-ignored media in `studio`).
3. **Verification Gate**: Specific `pytest`, `ruff check`, `publish build`, or `clerk agents status` checks that prove completion.
