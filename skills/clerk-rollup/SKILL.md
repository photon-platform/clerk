---
name: clerk-rollup
description: >-
  Audit, verify, document, version-bump, merge to main, tag, and push completed
  feature or fix branches across PHOTON and GEOMETOR repositories using Python 3.13
  uv sandbox checks and Sphinx publish builds.
---

# Clerk Rollup Workflow (`clerk-rollup`)

Use this runbook to finalize, verify, release, and tag changes from a `feature/*` or `fix/*` branch across one or more PHOTON or GEOMETOR repositories.

> **Subagent Note**: If you were instructed to commit on a feature branch *without* merging or pushing, execute **Steps 1–3** (and commit on the feature branch) and stop before Step 5.

---

## 1. Audit Branch Diff & Working Tree

Keep every command single-purpose and prefix-matchable (never chain with `&&`, `;`, `||`, or `cd`):

```bash
git -C /home/phi/PROJECTS/<org>/<repo> status
git -C /home/phi/PROJECTS/<org>/<repo> diff main...HEAD --stat
git -C /home/phi/PROJECTS/<org>/<repo> log main..HEAD --oneline
```

- Ensure no scratch files, temporary build artifacts (`slides_*/`, `frames_*/`, `*_stage.html`), or stray scripts are untracked or staged.
- If agent skills or subagent definitions were added or updated, verify symlink alignment:
  ```bash
  clerk agents status
  ```

---

## 2. Run Quality & Documentation Verification Gates

All checks run inside the sandbox (`BypassSandbox: false`) on `uv`-managed Python 3.13:

1. **Unit Tests**:
   ```bash
   uv run --no-sync pytest
   ```
2. **Lint & Type/Docstring Checks**:
   ```bash
   ruff check src tests
   ```
3. **Sphinx Documentation Build (`publish build`)**:
   Whenever `docsrc/`, docstrings, RST apparatus, or theme assets are affected, run `publish build` with `Cwd` set to the repository root and confirm zero broken references or Sphinx errors:
   ```bash
   publish build
   ```

---

## 3. Update Release Metadata & Progress Logs

When preparing a tagged release:

1. **Bump Semantic Version**:
   - Increment `__version__` in `src/<namespace>/<repo_name>/__init__.py` (`patch` for fixes, `minor` for new features/codices, `major` for breaking API changes).
2. **Update `CHANGELOG.rst`**:
   - Prepend a new `<X.Y.Z>` section (`-` underline) with today's ISO date (`*YYYY-MM-DD*`) and categorized entries (`**added**`, `**changed**`, `**fixed**`, `**refactored**`).
3. **Add Progress Log Entry (`docsrc/log/`)**:
   - If the repository maintains a Sphinx journal (`docsrc/log/index.rst`), create `docsrc/log/<YY.DDD-HHMMSS>/index.rst` with `:type: log`, `:date: <YY.DDD-HHMMSS>`, and `:author: phi`, summarizing architectural decisions and verification metrics.
4. **Sync `GEMINI.md` & `README.rst`**:
   - Update module indexes, CLI subcommands, and workflow notes if public behavior changed, then re-run `publish build` so `docs/` includes the updated changelog and log entry.

---

## 4. Commit Cleanly on the Feature Branch

Stage intentional changes and create a descriptive conventional commit:

```bash
git -C /home/phi/PROJECTS/<org>/<repo> add -A
git -C /home/phi/PROJECTS/<org>/<repo> commit -m "feat(<scope>): <concise summary> (vX.Y.Z)"
```

---

## 5. Merge to `main`, Tag, Push, and Prune Branch

When authorized to release to `main`:

1. **Merge & Tag Locally** (sandboxed):
   ```bash
   git -C /home/phi/PROJECTS/<org>/<repo> switch main
   git -C /home/phi/PROJECTS/<org>/<repo> merge <branch-name>
   git -C /home/phi/PROJECTS/<org>/<repo> tag vX.Y.Z
   ```
2. **Push to GitHub** (requires network access -> `BypassSandbox: true` ONLY on the `git push` commands):
   ```bash
   git -C /home/phi/PROJECTS/<org>/<repo> push origin main
   git -C /home/phi/PROJECTS/<org>/<repo> push origin vX.Y.Z
   ```
3. **Delete Merged Feature Branch**:
   ```bash
   git -C /home/phi/PROJECTS/<org>/<repo> branch -d <branch-name>
   ```
   For multi-repo releases, complete Steps 1–5 in dependency order (e.g., `model` $\rightarrow$ `elements` / `pappus`, or `publish` $\rightarrow$ scholarly codex repos).
