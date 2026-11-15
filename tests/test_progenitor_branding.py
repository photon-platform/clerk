"""Tests for brand logo.png and favicon.ico provisioning during clerk init."""

from __future__ import annotations

from pathlib import Path

from photon_platform.clerk.init.progenitor import create_project


def test_create_project_provisions_geometor_and_photon_brand_assets(tmp_path: Path) -> None:
    """Ensure create_project copies org-appropriate logo.png and favicon.ico."""
    create_project(
        github_id="geometor",
        package_namespace="geometor",
        github_repo_id="sample_geo",
        package_name="sample_geo",
        author="phi ARCHITECT",
        description="Sample GEOMETOR package",
        path=tmp_path,
    )
    geo_static = tmp_path / "sample_geo" / "docsrc" / "_static"
    assert (geo_static / "logo.png").is_file()
    assert (geo_static / "favicon.ico").is_file()

    create_project(
        github_id="photon-platform",
        package_namespace="photon_platform",
        github_repo_id="sample_photon",
        package_name="sample_photon",
        author="phi ARCHITECT",
        description="Sample PHOTON package",
        path=tmp_path,
    )
    ph_static = tmp_path / "sample_photon" / "docsrc" / "_static"
    assert (ph_static / "logo.png").is_file()
    assert (ph_static / "favicon.ico").is_file()
    assert (geo_static / "logo.png").read_bytes() != (ph_static / "logo.png").read_bytes()
    assert (geo_static / "favicon.ico").read_bytes() != (ph_static / "favicon.ico").read_bytes()
