:order: 2

modulator
=========

The ``modulator`` command shapes Python modules, classes, and functions.

Context Awareness
-----------------

Modulator automatically detects the project context to provide defaults for arguments:

- **Project Path**: inferred from the current working directory (looking for ``pyproject.toml`` or ``.git``).
- **Namespace**: inferred from the repository name (e.g. ``my-repo`` -> ``my_repo``).

If these cannot be detected, you will be prompted to provide them.

Usage
-----

.. click:: photon_platform.clerk.modulator.cli:modulator
   :prog: clerk modulator
   :nested: full
