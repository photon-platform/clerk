"""Catalog manifest loader and exact-symbolic validation helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

__all__ = [
    "CatalogEntrySpec",
    "assert_no_floats",
    "load_catalog_manifest",
]

_DEFAULT_MANIFEST = Path(__file__).resolve().parents[3] / "resources" / "catalog_manifest.json"


@dataclass(frozen=True, slots=True)
class CatalogEntrySpec:
    """Metadata descriptor for an atomic mathematical catalog entry."""

    id: str
    chapter: str
    title: str
    source_locus: str
    field: str = "Q(phi)"
    status: str = "planned"


def assert_no_floats(expr: object) -> None:
    """Raise ``TypeError`` if ``expr`` is a Python ``float`` or contains ``sympy.Float`` atoms.

    Args:
        expr: Python object or SymPy symbolic expression to inspect.

    Raises:
        TypeError: If any floating-point approximation is present.
    """
    if isinstance(expr, float):
        msg = f"Floating-point value forbidden in exact symbolic catalog: {expr!r}"
        raise TypeError(msg)
    atoms_fn = getattr(expr, "atoms", None)
    if callable(atoms_fn):
        for atom in atoms_fn():
            if atom.__class__.__name__ == "Float":
                msg = f"SymPy Float atom forbidden in exact symbolic catalog: {atom!r}"
                raise TypeError(msg)


def load_catalog_manifest(manifest_path: Path | None = None) -> list[CatalogEntrySpec]:
    """Load atomic catalog entries from ``resources/catalog_manifest.json``.

    Args:
        manifest_path: Optional override path to a catalog manifest JSON file.

    Returns:
        Ordered list of :class:`CatalogEntrySpec` records.
    """
    target = manifest_path or _DEFAULT_MANIFEST
    if not target.is_file():
        return []
    payload = json.loads(target.read_text(encoding="utf-8"))
    entries = payload.get("entries", []) if isinstance(payload, dict) else []
    return [
        CatalogEntrySpec(
            id=str(item["id"]),
            chapter=str(item.get("chapter", "")),
            title=str(item["title"]),
            source_locus=str(item.get("source_locus", "")),
            field=str(item.get("field", "Q(phi)")),
            status=str(item.get("status", "planned")),
        )
        for item in entries
    ]
