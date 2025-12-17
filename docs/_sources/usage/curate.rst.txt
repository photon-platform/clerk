:order: 3

curate
======

The ``curate`` command:
- **branches**: Lists branches.
- **create-release-branch**: Creates a release branch (e.g. `release-0.1.0`).
- **merge-to-main**: Merges a branch to main.
- **create-tag**: Creates a git tag.
- **rollup**: Automates the release process (version bump, changelog, merge, tag).
- **status**: Shows git status and diff since branching.

Context Awareness
-----------------

Curator operations default to the current **Project Root** if not explicitly provided.

- **Repo Path**: Defaults to the detected project root containing ``.git``.

Usage
-----

.. click:: photon_platform.clerk.curate.cli:curate
   :prog: clerk curate
   :nested: full
