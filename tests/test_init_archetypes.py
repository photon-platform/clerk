"""End-to-end tests for ``clerk init`` archetypes, context resolution, and log entries."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from photon_platform.clerk.clerk import cli
from photon_platform.clerk.context import determine_context
from photon_platform.clerk.init.progenitor import create_project
from photon_platform.clerk.log.logger import create_log_entry


def test_determine_context_at_org_root_with_workspace_pyproject(tmp_path: Path) -> None:
    """Ensure ~/PROJECTS/<org> resolves org_name even if a workspace pyproject.toml exists."""
    org_dir = tmp_path / "PROJECTS" / "geometor"
    org_dir.mkdir(parents=True)
    (org_dir / "pyproject.toml").write_text("[tool.uv.workspace]\nmembers = []\n", encoding="utf-8")

    ctx = determine_context(org_dir)
    assert ctx.org_name == "geometor"


def test_create_log_entry_renders_strict_variables(tmp_path: Path) -> None:
    """Verify create_log_entry populates date_code, author, and normalized tag lists."""
    entry_path = Path(
        create_log_entry(
            tmp_path,
            title="Test Milestone",
            excerpt="Verified strict log rendering.",
            tags="init, codex, verification",
            category="release",
            image="",
            author="phi ARCHITECT",
        )
    )
    assert entry_path.is_file()
    content = entry_path.read_text(encoding="utf-8")
    assert ":author: phi ARCHITECT" in content
    assert ":tags: init, codex, verification" in content
    assert ":categories: release" in content
    assert "Test Milestone" in content


@pytest.mark.parametrize("archetype", ["code", "codex", "catalog"])
def test_archetype_scaffolds_pass_pytest_and_ruff(tmp_path: Path, archetype: str) -> None:
    """Verify every archetype generates valid Python 3.13 code passing pytest and ruff."""
    repo_id = f"sample-{archetype}"
    project_path = create_project(
        github_id="geometor",
        package_namespace="geometor",
        github_repo_id=repo_id,
        package_name=repo_id,
        author="phi ARCHITECT",
        description=None,
        path=tmp_path,
        archetype=archetype,
        edition_slug="tractatus" if archetype == "codex" else None,
        book_title="De Proporzione Test",
        book_author="Euclid of Alexandria",
        git_init=True,
    )
    assert project_path is not None
    assert project_path == tmp_path / repo_id
    assert (project_path / ".git").is_dir()

    pkg_dir = project_path / "src" / "geometor" / f"sample_{archetype}"
    assert (pkg_dir / "__init__.py").is_file()
    assert (pkg_dir / "app.py").is_file()
    assert (pkg_dir / "__main__.py").is_file()
    assert (project_path / "GEMINI.md").is_file()
    assert (project_path / "ROADMAP.md").is_file()
    assert "None" not in (project_path / "pyproject.toml").read_text(encoding="utf-8")
    assert "Copyright (c)  " not in (project_path / "LICENSE").read_text(encoding="utf-8")

    readme_txt = (project_path / "README.rst").read_text(encoding="utf-8")
    assert f"GEOMETOR • {repo_id}" in readme_txt
    assert f"**Visit the Online Archive:** https://geometor.github.io/{repo_id}/" in readme_txt

    if archetype == "codex":
        assert "Euclid of Alexandria • De Proporzione Test • semantic digital archive" in readme_txt
        assert (project_path / "docsrc" / "tractatus" / "index.rst").is_file()
        codex_idx = (project_path / "docsrc" / "tractatus" / "index.rst").read_text(encoding="utf-8")
        assert ":type: book" in codex_idx
        assert "structure_map.json" not in codex_idx
        home_idx = (project_path / "docsrc" / "index.rst").read_text(encoding="utf-8")
        assert "semantic digital archive • the works of" in home_idx
        assert "Euclid of Alexandria" in home_idx
        conf_txt = (project_path / "docsrc" / "conf.py").read_text(encoding="utf-8")
        assert 'site_title = "Euclid of Alexandria"' in conf_txt
        assert (project_path / "resources" / "tractatus" / "structure_map.json").is_file()
        smap = json.loads(
            (project_path / "resources" / "tractatus" / "structure_map.json").read_text(
                encoding="utf-8"
            )
        )
        assert smap["edition"] == "tractatus"
    elif archetype == "catalog":
        assert "Euclid of Alexandria • De Proporzione Test • semantic digital archive" in readme_txt
        home_idx = (project_path / "docsrc" / "index.rst").read_text(encoding="utf-8")
        assert "semantic digital archive • mathematical catalog" in home_idx
        action_txt = (project_path / ".github" / "workflows" / "action.yml").read_text(
            encoding="utf-8"
        )
        assert "https://github.com/geometor/model.git" in action_txt
        assert (pkg_dir / "catalog.py").is_file()
        assert (project_path / "docsrc" / "catalog" / "index.rst").is_file()
        assert (project_path / "resources" / "catalog_manifest.json").is_file()
        assert (project_path / "resources" / "concordance.json").is_file()

    # Run pytest on the generated project
    pytest_res = subprocess.run(
        [sys.executable, "-m", "pytest"],
        cwd=project_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert pytest_res.returncode == 0, pytest_res.stdout + pytest_res.stderr

    # Run ruff check on the generated project if ruff is installed
    ruff_bin = shutil.which("ruff")
    if ruff_bin:
        ruff_res = subprocess.run(
            [ruff_bin, "check", "src", "tests", "demos"],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=False,
        )
        assert ruff_res.returncode == 0, ruff_res.stdout + ruff_res.stderr


def test_cli_init_and_publish_build(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify ``clerk init`` CLI creates a catalog repo that compiles cleanly with publish."""
    org_dir = tmp_path / "PROJECTS" / "geometor"
    org_dir.mkdir(parents=True)
    monkeypatch.chdir(org_dir)

    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "init",
            "golden-sample",
            "--type",
            "catalog",
            "--title",
            "Golden Sample Catalog",
            "--book-author",
            "phi ARCHITECT",
        ],
    )
    assert result.exit_code == 0, result.output
    repo_dir = org_dir / "golden-sample"
    assert (repo_dir / ".git").is_dir()
    assert (repo_dir / "docsrc" / "catalog" / "index.rst").is_file()

    publish_bin = shutil.which("publish")
    if publish_bin:
        pub_res = subprocess.run(
            [publish_bin, "build"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        assert pub_res.returncode == 0, pub_res.stdout + pub_res.stderr
        assert "WARNING:" not in pub_res.stderr, pub_res.stderr
        assert (repo_dir / "docs" / "html" / "index.html").is_file() or (
            repo_dir / "docs" / "index.html"
        ).is_file()
