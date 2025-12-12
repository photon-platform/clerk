:order: 5

logger
======

The ``logger`` command creates standardized log entries in the project's documentation.

Context Awareness
-----------------

Logger **requires** a valid project context to function.

- **Project Root**: Detected by traversing up the directory tree.
- **Log Location**: Log entries are automatically written to ``<project_root>/docsrc/log/<timestamp>/``.

Usage
-----

.. click:: photon_platform.clerk.logger.cli:logger
   :prog: clerk logger
   :nested: full
