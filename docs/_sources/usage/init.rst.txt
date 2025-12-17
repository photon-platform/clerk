:order: 1

init
====

The ``init`` command creates new Python projects using standard templates.

Context Awareness
-----------------

Progenitor uses the current working directory to determine the **Organization** context. It expects to be run within a directory structure like ``~/PROJECTS/<organization>/``.

- **Organization**: Inferred from the parent directory of the new project.

Usage
-----

.. click:: photon_platform.clerk.init.cli:init
   :prog: clerk init
   :nested: full
