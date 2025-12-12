:order: 5

log
===

The ``log`` command creates standardized log entries in the project's documentation.

Context Awareness
-----------------

Logger **requires** a valid project context to function.

- **Project Root**: Detected by traversing up the directory tree.
- **Log Location**: Log entries are automatically written to ``<project_root>/docsrc/log/<timestamp>/``.

Usage
-----

.. click:: photon_platform.clerk.log.cli:log
   :prog: clerk log
   :nested: full
