"""Unit tests for `photon_platform.clerk.agents` discovery, status, and symlink sync."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from photon_platform.clerk.agents import (
    check_status,
    discover_customizations,
    sync_links,
)
from photon_platform.clerk.clerk import cli


def _write_skill(repo_dir: Path, name: str) -> Path:
    skill_dir = repo_dir / "skills" / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Test skill {name}\n---\n# {name}\n",
        encoding="utf-8",
    )
    return skill_dir


def _write_agent(repo_dir: Path, filename: str) -> Path:
    agents_dir = repo_dir / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    agent_file = agents_dir / filename
    stem = filename.removesuffix(".md")
    agent_file.write_text(
        f"---\nname: {stem}\ndescription: Test agent {stem}\n---\nAgent body.\n",
        encoding="utf-8",
    )
    return agent_file


def _scaffold_projects(tmp_path: Path) -> tuple[Path, Path]:
    projects_dir = tmp_path / "PROJECTS"
    global_cfg = tmp_path / "gemini_config"

    clerk_repo = projects_dir / "photon-platform" / "clerk"
    publish_repo = projects_dir / "photon-platform" / "publish"
    studio_repo = projects_dir / "photon-platform" / "studio"
    geometor_cfg = projects_dir / "geometor" / ".config"

    _write_skill(clerk_repo, "clerk-branch")
    _write_skill(clerk_repo, "clerk-rollup")
    _write_agent(clerk_repo, "clerk.md")

    _write_skill(publish_repo, "scriptorium-codex")
    _write_agent(publish_repo, "scriptorium.md")

    _write_skill(geometor_cfg, "geometor-construct")
    _write_agent(geometor_cfg, "geometer.md")

    _write_skill(studio_repo, "studio")
    _write_agent(studio_repo, "studio.md")
    # Simulate legacy accidental copies inside studio that must be ignored
    _write_skill(studio_repo, "clerk-branch")
    _write_skill(studio_repo, "podcaster")
    _write_agent(studio_repo, "podcaster.md")

    return projects_dir, global_cfg


def test_discover_customizations_ignores_retired_studio_copies(tmp_path: Path) -> None:
    """Ensure canonical owners win and retired studio copies are excluded."""
    projects_dir, _ = _scaffold_projects(tmp_path)
    items, collisions = discover_customizations(projects_dir=projects_dir)

    assert not collisions
    skills = {i.name: i.repo for i in items if i.kind == "skill"}
    agents_map = {i.name: i.repo for i in items if i.kind == "agent"}

    assert skills == {
        "clerk-branch": "photon-platform/clerk",
        "clerk-rollup": "photon-platform/clerk",
        "scriptorium-codex": "photon-platform/publish",
        "geometor-construct": "geometor/.config",
        "studio": "photon-platform/studio",
    }
    assert agents_map == {
        "clerk.md": "photon-platform/clerk",
        "scriptorium.md": "photon-platform/publish",
        "geometer.md": "geometor/.config",
        "studio.md": "photon-platform/studio",
    }
    assert all(i.source_exists for i in items)


def test_sync_replaces_stale_copies_and_verifies_status(tmp_path: Path) -> None:
    """Verify `sync_links` converts disconnected copies into clean symlinks."""
    projects_dir, global_cfg = _scaffold_projects(tmp_path)

    # Create a disconnected stale copy in global config and a wrong symlink in geometor
    stale_skill = global_cfg / "skills" / "clerk-branch"
    stale_skill.mkdir(parents=True)
    (stale_skill / "SKILL.md").write_text("stale copy", encoding="utf-8")

    wrong_agent_dir = projects_dir / "geometor" / ".agents" / "agents"
    wrong_agent_dir.mkdir(parents=True)
    wrong_target = tmp_path / "wrong_clerk.md"
    wrong_target.write_text("wrong", encoding="utf-8")
    (wrong_agent_dir / "clerk.md").symlink_to(wrong_target)

    pre_status = check_status(projects_dir=projects_dir, global_config_dir=global_cfg)
    assert not pre_status.all_ok
    by_target_name = {(c.target_label, c.name): c.status for c in pre_status.checks}
    assert by_target_name[("global:gemini-config", "clerk-branch")] == "stale_copy"
    assert by_target_name[("workspace:geometor", "clerk.md")] == "wrong_target"

    # Dry-run should not mutate disk
    dry_report = sync_links(
        projects_dir=projects_dir,
        global_config_dir=global_cfg,
        dry_run=True,
    )
    assert dry_report.ok
    assert not stale_skill.is_symlink()

    # Real sync replaces stale copy and retargets wrong symlink
    sync_report = sync_links(projects_dir=projects_dir, global_config_dir=global_cfg)
    assert sync_report.ok
    assert stale_skill.is_symlink()
    assert (wrong_agent_dir / "clerk.md").resolve() == (
        projects_dir / "photon-platform" / "clerk" / "agents" / "clerk.md"
    ).resolve()

    post_status = check_status(projects_dir=projects_dir, global_config_dir=global_cfg)
    assert post_status.all_ok


def test_cli_status_and_sync_json(tmp_path: Path) -> None:
    """Test `clerk agents sync` and `clerk agents status --strict --json` via Click."""
    projects_dir, global_cfg = _scaffold_projects(tmp_path)
    runner = CliRunner()

    fail_res = runner.invoke(
        cli,
        [
            "agents",
            "status",
            "--projects-dir",
            str(projects_dir),
            "--global-config-dir",
            str(global_cfg),
            "--strict",
            "--json",
        ],
    )
    assert fail_res.exit_code == 1
    fail_payload = json.loads(fail_res.output)
    assert fail_payload["all_ok"] is False

    sync_res = runner.invoke(
        cli,
        [
            "agents",
            "sync",
            "--projects-dir",
            str(projects_dir),
            "--global-config-dir",
            str(global_cfg),
            "--json",
        ],
    )
    assert sync_res.exit_code == 0, sync_res.output
    sync_payload = json.loads(sync_res.output)
    assert sync_payload["ok"] is True

    ok_res = runner.invoke(
        cli,
        [
            "agents",
            "status",
            "--projects-dir",
            str(projects_dir),
            "--global-config-dir",
            str(global_cfg),
            "--strict",
            "--json",
        ],
    )
    assert ok_res.exit_code == 0, ok_res.output
    ok_payload = json.loads(ok_res.output)
    assert ok_payload["all_ok"] is True


def test_pending_source_and_prune_unmanaged(tmp_path: Path) -> None:
    """Verify pending canonical files link cleanly and `--prune` removes stray entries."""
    projects_dir, global_cfg = _scaffold_projects(tmp_path)
    # Remove studio.md to simulate an in-flight parallel branch
    (projects_dir / "photon-platform" / "studio" / "agents" / "studio.md").unlink()

    # Add an unmanaged skill in geometor/.agents
    stray = projects_dir / "geometor" / ".agents" / "skills" / "old-stray-skill"
    stray.mkdir(parents=True)
    (stray / "SKILL.md").write_text("stray", encoding="utf-8")

    sync_res = sync_links(
        projects_dir=projects_dir,
        global_config_dir=global_cfg,
        scope="workspaces",
        prune_unmanaged=True,
    )
    assert sync_res.ok
    assert not stray.exists()

    ws_status = check_status(
        projects_dir=projects_dir,
        global_config_dir=global_cfg,
        scope="workspaces",
    )
    studio_checks = [c for c in ws_status.checks if c.name == "studio.md"]
    assert len(studio_checks) == 2
    assert all(c.status == "pending_source" for c in studio_checks)
    assert not ws_status.unmanaged_checks

