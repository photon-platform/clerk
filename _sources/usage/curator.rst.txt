:order: 3

curator
=======

The ``curator`` command manages git repositories, branches, and releases.

Context Awareness
-----------------

Curator operations default to the current **Project Root** if not explicitly provided.

- **Repo Path**: Defaults to the detected project root containing ``.git``.

Usage
-----

.. click:: photon_platform.clerk.curator.cli:curator
   :prog: clerk curator
   :nested: full
