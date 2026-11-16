"""Repository scaffolding engine supporting code, codex, and catalog archetypes."""

from __future__ import annotations

import shutil
import subprocess
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from jinja2 import Environment, PackageLoader, StrictUndefined

from photon_platform.clerk.build.modulator import Modulator

ARCHETYPES: tuple[str, ...] = ("code", "codex", "catalog")

__all__ = [
    "ARCHETYPES",
    "create_project",
]


def _clean_identifier(value: str) -> str:
    """Normalize a string into a snake_case Python identifier."""
    cleaned = value.strip().replace("-", "_").replace(" ", "_").replace(".", "_")
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_") or "pkg"


def _resolve_org_title(github_id: str, package_namespace: str) -> str:
    """Resolve human-facing organization brand title."""
    tokens = {github_id.strip().lower(), package_namespace.strip().lower()}
    if "geometor" in tokens:
        return "GEOMETOR"
    if any("photon" in token for token in tokens):
        return "PHOTON"
    return github_id.strip()


def _copy_brand_assets(
    project_path: Path,
    github_id: str,
    package_namespace: str,
    script_dir: Path,
) -> None:
    """Copy canonical org ``logo.png`` and ``favicon.ico`` into ``docsrc/_static/``."""
    tokens = {str(github_id).strip().lower(), str(package_namespace).strip().lower()}
    org_key = "geometor" if "geometor" in tokens else "photon-platform"
    assets_dir = script_dir / "assets" / org_key
    target_static = project_path / "docsrc" / "_static"
    target_static.mkdir(parents=True, exist_ok=True)
    for filename in ("logo.png", "favicon.ico"):
        src = assets_dir / filename
        if src.is_file():
            shutil.copy2(src, target_static / filename)


def _default_topics(archetype: str, has_explicit_book_author: bool) -> list[str]:
    """Return canonical GitHub topic pills for the given repository archetype."""
    if archetype == "codex":
        return ["books", "people"] if has_explicit_book_author else ["books"]
    if archetype == "catalog":
        return ["catalogs", "people"] if has_explicit_book_author else ["catalogs"]
    return ["modules"]


def _default_description(
    archetype: str,
    org_title: str,
    github_repo_id: str,
    resolved_title: str,
    resolved_book_author: str,
    has_explicit_book_author: bool,
) -> str:
    """Construct a clean default repository description when none is supplied."""
    if org_title == "GEOMETOR":
        if archetype == "codex":
            if has_explicit_book_author:
                return f"{resolved_book_author} • {resolved_title} • semantic digital archive"
            return f"{resolved_title} • semantic digital archive"
        if archetype == "catalog":
            if has_explicit_book_author:
                return f"{resolved_book_author} • {resolved_title} • semantic digital archive"
            return f"{resolved_title} • Mathematical Catalog • semantic digital archive"
        return f"{resolved_title} • GEOMETOR symbolic module"
    return f"{org_title} • {github_repo_id} package"



def create_project(
    github_id: str,
    package_namespace: str,
    github_repo_id: str,
    package_name: str,
    author: str,
    description: str | None,
    path: str | Path,
    *,
    archetype: str = "code",
    edition_slug: str | None = None,
    book_title: str | None = None,
    book_author: str | None = None,
    git_init: bool = False,
) -> Path | None:
    """Create a new Python 3.13 project repository from archetype templates.

    Args:
        github_id: GitHub organization or account slug (e.g. ``"geometor"``).
        package_namespace: Top-level Python namespace package (e.g. ``"geometor"``).
        github_repo_id: Repository folder and GitHub slug (preserves hyphens).
        package_name: Python package name under ``src/<package_namespace>/``.
        author: Maintainer / copyright holder name.
        description: One-line repository summary (auto-populated if ``None`` or empty).
        path: Parent directory in which ``<github_repo_id>/`` will be created.
        archetype: One of ``"code"``, ``"codex"``, or ``"catalog"``.
        edition_slug: Primary codex edition directory slug (defaults to ``package_name``).
        book_title: Optional scholarly treatise or catalog display title.
        book_author: Optional primary historical or curated author attribution.
        git_init: If ``True``, initialize a git repository on branch ``main``.

    Returns:
        Created ``project_path`` :class:`~pathlib.Path`, or ``None`` if target already exists.

    Raises:
        ValueError: If ``archetype`` is not one of :data:`ARCHETYPES`.
    """
    normalized_archetype = archetype.strip().lower()
    if normalized_archetype not in ARCHETYPES:
        valid = ", ".join(ARCHETYPES)
        msg = f"Unsupported archetype {archetype!r}; expected one of: {valid}"
        raise ValueError(msg)

    repo_folder_name = str(github_repo_id).strip()
    clean_namespace = _clean_identifier(str(package_namespace))
    clean_pkg_name = _clean_identifier(str(package_name))
    clean_edition = _clean_identifier(edition_slug) if edition_slug else clean_pkg_name

    project_path = Path(path) / repo_folder_name
    if project_path.exists():
        print(f"Error: The path {project_path} already exists.")
        return None
    project_path.mkdir(parents=True)

    clean_author = (author or "phi ARCHITECT").strip()
    org_title = _resolve_org_title(str(github_id), clean_namespace)
    resolved_title = (
        book_title.strip()
        if book_title and book_title.strip()
        else repo_folder_name.replace("-", " ").replace("_", " ").title()
    )
    has_explicit_book_author = bool(book_author and book_author.strip())
    resolved_book_author = book_author.strip() if has_explicit_book_author else clean_author

    clean_description = (
        description.strip()
        if description and description.strip()
        else _default_description(
            archetype=normalized_archetype,
            org_title=org_title,
            github_repo_id=repo_folder_name,
            resolved_title=resolved_title,
            resolved_book_author=resolved_book_author,
            has_explicit_book_author=has_explicit_book_author,
        )
    )

    modulator = Modulator(project_path, clean_namespace)
    modulator.create_module(
        clean_pkg_name,
        description=clean_description,
        cli_name=repo_folder_name,
        author=clean_author,
        archetype=normalized_archetype,
    )

    today = date.today()
    init_code = today.strftime("%y.%j")
    author_email = (
        "github@geometor.com" if org_title == "GEOMETOR" else "github@phiarchitect.com"
    )

    if normalized_archetype == "codex" and has_explicit_book_author:
        human_site_title = resolved_book_author
    else:
        human_site_title = resolved_title

    template_variables: dict[str, Any] = {
        "author": clean_author,
        "author_name": clean_author,
        "author_email": author_email,
        "github_id": str(github_id).strip(),
        "org_name": str(github_id).strip(),
        "org_title": org_title,
        "org_slug": clean_namespace,
        "github_repo_id": repo_folder_name,
        "repo_name": repo_folder_name,
        "project_name": repo_folder_name,
        "package_namespace": clean_namespace,
        "package_name": clean_pkg_name,
        "repo_slug": clean_pkg_name,
        "description": clean_description,
        "summary": clean_description.rstrip("."),
        "current_year": str(today.year),
        "iso_date": today.isoformat(),
        "init": init_code,
        "log_stamp": f"{init_code}-000000",
        "archetype": normalized_archetype,
        "edition_slug": clean_edition,
        "book_title": resolved_title,
        "book_author": resolved_book_author,
        "site_title": human_site_title,
        "home_heading": human_site_title,
        "live_url": f"https://{str(github_id).strip()}.github.io/{repo_folder_name}/",
        "github_topics": _default_topics(normalized_archetype, has_explicit_book_author),
    }

    env = Environment(
        loader=PackageLoader("photon_platform.clerk.init"),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    script_dir = Path(__file__).parent.resolve()
    yaml_file_path = script_dir / "templates.yaml"
    with yaml_file_path.open(encoding="utf-8") as handle:
        file_structure: list[dict[str, Any]] = yaml.safe_load(handle)

    for file_info in file_structure:
        allowed_archetypes = file_info.get("archetypes")
        if allowed_archetypes is not None and normalized_archetype not in allowed_archetypes:
            continue
        rendered_rel_target = env.from_string(file_info["target"]).render(template_variables)
        target = project_path / rendered_rel_target
        target.parent.mkdir(parents=True, exist_ok=True)
        template = env.get_template(file_info["template"])
        target.write_text(template.render(template_variables), encoding="utf-8")

    _copy_brand_assets(project_path, str(github_id).strip(), clean_namespace, script_dir)
    try:
        from photon_platform.publish.social_meta import generate_repo_social_banners

        generate_repo_social_banners(project_path)
    except ImportError:
        pass

    if git_init:
        subprocess.run(
            ["git", "-C", str(project_path), "init", "-b", "main"],
            check=True,
            capture_output=True,
            text=True,
        )

    return project_path
