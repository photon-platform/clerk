:order: 1

progenitor
==========

The ``progenitor`` command creates new Python projects using standard templates.

Context Awareness
-----------------

Progenitor uses the current working directory to determine the **Organization** context. It expects to be run within a directory structure like ``~/PROJECTS/<organization>/``.

- **Organization**: Inferred from the parent directory of the new project.

Usage
-----

.. click:: photon_platform.clerk.progenitor.cli:progenitor
   :prog: clerk progenitor
   :nested: full
