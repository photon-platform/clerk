"""Python namespace package and module scaffolder for Clerk."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, StrictUndefined

__all__ = ["Modulator"]


def _wrap_string_literal(text: str, width: int = 68, indent: str = "        ") -> str:
    """Format an arbitrary string as an indented Python implicit string-literal concatenation."""
    if len(text) <= width:
        return json.dumps(text)
    chunks = textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )
    if not chunks:
        return '""'
    pieces = [
        f"{chunk} " if idx < len(chunks) - 1 else chunk for idx, chunk in enumerate(chunks)
    ]
    joined = f"\n{indent}".join(json.dumps(piece) for piece in pieces)
    return f"(\n{indent}{joined}\n    )"


class Modulator:
    """Generate Python 3.13 namespace modules and CLI entry points."""

    def __init__(self, project_path: Path, namespace: str) -> None:
        """Initialize a modulator rooted at ``project_path``.

        Args:
            project_path: Repository root directory containing ``src/``.
            namespace: Top-level PEP 420 namespace package name.
        """
        self.project_path = Path(project_path)
        self.namespace = self._clean(namespace)
        self.env = Environment(
            loader=PackageLoader("photon_platform.clerk.build", "templates"),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
        )

    def create_module(
        self,
        module_name: str,
        *,
        description: str | None = None,
        cli_name: str | None = None,
        author: str = "phi ARCHITECT",
        archetype: str = "code",
    ) -> Path:
        """Scaffold ``src/<namespace>/<module_name>/`` with ``__init__``, ``app``, and ``__main__``.

        Args:
            module_name: Python module or dotted submodule identifier.
            description: Human-readable package summary for module docstrings and ``--help``.
            cli_name: Console-script display name (defaults to ``module_name``).
            author: Author name for metadata.
            archetype: Repository archetype (``"code"``, ``"codex"``, or ``"catalog"``).

        Returns:
            Directory path of the created Python package.
        """
        parts = [self._clean(part) for part in module_name.split(".") if part.strip()]
        leaf_name = parts[-1]
        module_rel = Path(*parts)
        module_dir = self.project_path / "src" / self.namespace / module_rel
        module_dir.mkdir(parents=True, exist_ok=True)

        clean_desc = (description or f"{self.namespace}.{leaf_name} package").strip()
        summary = clean_desc.rstrip(".")

        context: dict[str, Any] = {
            "namespace_name": self.namespace,
            "module_name": ".".join(parts),
            "leaf_name": leaf_name,
            "cli_name": cli_name or leaf_name.replace("_", "-"),
            "description": clean_desc,
            "description_literal": _wrap_string_literal(clean_desc),
            "summary": summary,
            "author": author,
            "archetype": archetype,
        }
        self._render_template("__init__.py.j2", context, module_dir / "__init__.py")
        self._render_template("__main__.py.j2", context, module_dir / "__main__.py")
        self._render_template("app.py.j2", context, module_dir / "app.py")
        return module_dir

    def create_submodule(self, module_name: str, submodule_name: str) -> Path:
        """Create a nested submodule under ``module_name``.

        Args:
            module_name: Parent package name.
            submodule_name: Child submodule name.

        Returns:
            Directory path of the created submodule.
        """
        return self.create_module(f"{self._clean(module_name)}.{self._clean(submodule_name)}")

    def create_class(self, module_name: str, class_name: str) -> Path:
        """Create a standalone Python 3.13 class module stub.

        Args:
            module_name: Target package name under ``src/<namespace>/``.
            class_name: Class name to scaffold.

        Returns:
            Filesystem path of the created class module.
        """
        clean_mod = self._clean(module_name)
        clean_cls = self._clean(class_name)
        pascal_name = "".join(part.capitalize() for part in clean_cls.split("_") if part)
        module_dir = self.project_path / "src" / self.namespace / clean_mod
        module_dir.mkdir(parents=True, exist_ok=True)
        class_file = module_dir / f"{clean_cls}.py"
        content = (
            f'"""{pascal_name} definition for ``{self.namespace}.{clean_mod}``."""\n\n'
            "from __future__ import annotations\n\n"
            "from dataclasses import dataclass\n\n"
            f'__all__ = ["{pascal_name}"]\n\n\n'
            "@dataclass\n"
            f"class {pascal_name}:\n"
            f'    """Represent a {pascal_name} instance."""\n'
        )
        class_file.write_text(content, encoding="utf-8")
        return class_file

    def create_function(
        self,
        module_name: str,
        function_name: str,
        args: str,
        return_type: str,
    ) -> Path:
        """Append a typed function stub to ``<module_name>.py``.

        Args:
            module_name: Target package name under ``src/<namespace>/``.
            function_name: Function identifier.
            args: Parameter signature string.
            return_type: Return type annotation string.

        Returns:
            Filesystem path of the updated module file.
        """
        clean_mod = self._clean(module_name)
        clean_fn = self._clean(function_name)
        module_dir = self.project_path / "src" / self.namespace / clean_mod
        module_dir.mkdir(parents=True, exist_ok=True)
        function_file = module_dir / f"{clean_mod}.py"
        header = (
            ""
            if function_file.exists()
            else (
                f'"""Functions for ``{self.namespace}.{clean_mod}``."""\n\n'
                "from __future__ import annotations\n"
            )
        )
        ret = return_type.strip() or "None"
        snippet = (
            f"{header}\n\ndef {clean_fn}({args}) -> {ret}:\n"
            f'    """Execute ``{clean_fn}``."""\n'
            "    raise NotImplementedError\n"
        )
        with function_file.open("a", encoding="utf-8") as handle:
            handle.write(snippet)
        return function_file

    def create_class_method(
        self,
        module_name: str,
        class_name: str,
        method_name: str,
        args: str,
        return_type: str,
    ) -> Path:
        """Append a typed method stub to an existing class file.

        Args:
            module_name: Target package name under ``src/<namespace>/``.
            class_name: Target class module name.
            method_name: Method identifier.
            args: Parameter signature string (excluding ``self``).
            return_type: Return type annotation string.

        Returns:
            Filesystem path of the updated class file.
        """
        clean_mod = self._clean(module_name)
        clean_cls = self._clean(class_name)
        clean_method = self._clean(method_name)
        module_dir = self.project_path / "src" / self.namespace / clean_mod
        class_file = module_dir / f"{clean_cls}.py"
        if not class_file.exists():
            self.create_class(clean_mod, clean_cls)
        ret = return_type.strip() or "None"
        param_str = f"self, {args}" if args.strip() else "self"
        snippet = (
            f"\n    def {clean_method}({param_str}) -> {ret}:\n"
            f'        """Execute ``{clean_method}``."""\n'
            "        raise NotImplementedError\n"
        )
        with class_file.open("a", encoding="utf-8") as handle:
            handle.write(snippet)
        return class_file

    def _render_template(
        self,
        template_name: str,
        context: dict[str, Any],
        output_path: Path,
        mode: str = "w",
    ) -> None:
        template = self.env.get_template(template_name)
        with output_path.open(mode, encoding="utf-8") as handle:
            handle.write(template.render(**context))

    def _clean(self, name: str) -> str:
        return name.strip().replace(" ", "_").replace("-", "_")
