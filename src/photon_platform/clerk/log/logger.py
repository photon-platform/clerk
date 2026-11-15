"""PHOTON chronological Sphinx log entry generator."""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader, StrictUndefined

__all__ = [
    "LOG_TEMPLATE",
    "create_log_entry",
]

LOG_TEMPLATE = "log.rst.j2"


def _normalize_tags(tags: str | Iterable[str] | None) -> list[str]:
    """Normalize comma-delimited or iterable tags into a clean list of strings."""
    if tags is None:
        return []
    if isinstance(tags, str):
        return [token.strip() for token in tags.split(",") if token.strip()]
    return [str(token).strip() for token in tags if str(token).strip()]


def create_log_entry(
    project_root: Path | str,
    title: str,
    excerpt: str = "",
    tags: str | Iterable[str] | None = None,
    category: str = "",
    image: str = "",
    author: str = "phi ARCHITECT",
) -> str:
    """Create a timestamped RST log entry in ``<project_root>/docsrc/log/``.

    Args:
        project_root: Root directory of the target repository.
        title: Heading title for the log entry.
        excerpt: Short introductory body or summary text.
        tags: Comma-separated tag string or iterable of tag strings.
        category: Optional log category string.
        image: Optional relative image path.
        author: Author credit recorded in the ``:author:`` field list.

    Returns:
        Filesystem path string to the generated ``index.rst`` log file.
    """
    root = Path(project_root)
    log_time = datetime.now()
    log_stamp = log_time.strftime("%y.%j-%H%M%S")
    normalized_tags = _normalize_tags(tags)

    context = {
        "log_stamp": log_stamp,
        "date_code": log_stamp,
        "author": author,
        "title": title,
        "excerpt": excerpt,
        "tags": normalized_tags,
        "category": category,
        "image": image,
    }

    env = Environment(
        loader=PackageLoader("photon_platform.clerk.log"),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    template = env.get_template(LOG_TEMPLATE)
    rst_text = template.render(**context)

    entry_dir = root / "docsrc" / "log" / log_stamp
    entry_dir.mkdir(parents=True, exist_ok=True)

    filename = entry_dir / "index.rst"
    filename.write_text(rst_text, encoding="utf-8")

    return str(filename)
