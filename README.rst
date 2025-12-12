PHOTON • clerk
==============

The CLERK project is a pivotal component of the `PHOTON platform`_, a suite of
tools committed to gathering, processing, and publishing knowledge. Inspired by
Douglas Engelbart's vision of the computer as a "clerk" in his seminal paper,
`Augmenting Human Intellect`_, CLERK is a powerful command-line tool, designed
to provide situational awareness and context-sensitive operations based on the
current working directory (CWD) and the information it contains.

Here are the roles of CLERK, each fulfilling a unique function within the
knowledge management process:

- ``init``: Sparks life into Python projects.
- ``build``: Shapes Python modules and packages.
- ``curate``: Organizes git/archive management.
- ``log``: Creates log entries.
- ``gather``: Downloads and organizes information from the web. It can handle various sources like URLs, GitHub repositories, arXiv papers, and YouTube videos.

Usage
-----

CLERK is designed to be agent-friendly, supporting command-line arguments for all operations to enable non-interactive use.

Top-Level Commands
~~~~~~~~~~~~~~~~~~

- ``clerk gather``: Gathers content from various sources.
- ``clerk log``: Creates a new log entry.
- ``clerk init``: Creates a new Python project.
- ``clerk build``: Shapes Python modules and packages.
- ``clerk curate``: Organizes git/archive management.


``log`` Command
~~~~~~~~~~~~~~~

Creates a new log entry in ``docsrc/log/``.

.. code-block:: bash

    clerk log [OPTIONS]

Options:
    --title TEXT     Title for log entry
    --excerpt TEXT   Short description
    --tags TEXT      Comma separated list of tags
    --category TEXT  Comma separated list of categories
    --image TEXT     Path to image

``init`` Command
~~~~~~~~~~~~~~~~

Creates a new Python project structure.
Context awareness: Infers organization from parent directory and author from git config.

.. code-block:: bash

    clerk init [OPTIONS]

Options:
    --project-name TEXT  The name of the project.
    --description TEXT   A short description of the project.

``build`` Commands
~~~~~~~~~~~~~~~~~~

Shapes Python modules and packages.
Context awareness: Infers project path and namespace from CWD.

- `module`: Creates a new Python module.
- `submodule`: Creates a new Python submodule.
- `class`: Creates a new Python class.
- `function`: Creates a new Python function.
- `method`: Creates a new Python class method.

.. code-block:: bash

    clerk build module --module-name my_module
    clerk build function --module-name my_module --function-name my_func --args "a,b" --return-type int

``curate`` Commands
~~~~~~~~~~~~~~~~~~~

Manages git repositories and releases.
Context awareness: Infers repo path from CWD.

- `branches`: Lists branches.
- `create-release-branch`: Creates a release branch (e.g. `release-0.1.0`).
- `merge-to-main`: Merges a branch to main.
- `create-tag`: Creates a git tag.
- `rollup`: Automates the release process.
- `status`: Shows git status and diff.

.. code-block:: bash

    clerk curate create-release-branch --release-version 0.1.0 --description "New features"
    clerk curate rollup
    clerk curate status

`gather` Commands
~~~~~~~~~~~~~~~~~

Downloads and organizes information from the web.
Context awareness: Context Agnostic.

- `url`: Gathers content from a URL. It intelligently handles sources like Wikipedia, arXiv, YouTube, GitHub, and general web pages.
- `repo`: Gathers information about a GitHub repository (e.g., `owner/repo`).

.. code-block:: bash

    clerk gather url "https://example.com"
    clerk gather repo "photon-platform/clerk"

By being context-aware, CLERK can suggest relevant operations based on the CWD,
making workflows smoother and more efficient. This context-sensitive approach
elevates CLERK from a mere assistant to an enhancer of smarter workflows and a
partner in intellectual work.

As a part of the `PHOTON platform`_, CLERK contributes to the overarching mission
of knowledge gathering, processing, and publishing. It embodies the platform's
vision of enhancing work efficiency, productivity, and insight through
leveraging technology. In the spirit of Engelbart's vision, CLERK is designed
to augment your intellect, enabling you to focus on what matters most: creating
and sharing knowledge.

.. _`Augmenting Human Intellect`: https://www.dougengelbart.org/pubs/augment-3906.html

About PHOTON Platform
---------------------

The `PHOTON platform`_ is part of a comprehensive vision by `phi ARCHITECT`_ to
establish a system architecture for gathering, processing, and publishing
living digital archives. It is an integrated suite of open-source tools,
curated and customized for efficient and effective knowledge management.

Gather • Process • Publish
--------------------------
*Tools to shine brighter*

The `PHOTON platform`_, along with sister organizations `GEOMETOR`_ and `HARMONIC
resonance`_, works under the guiding principle of transforming complex
hierarchical content into accessible knowledge. With the aim of making order
and organization integral to the framework, the `PHOTON platform`_ thrives on
achieving mastery in all practices required for the mission.

For more details on the platform and its various projects, please visit our
`website`_ or explore our `GitHub organization`_.

The `PHOTON platform`_ is one of three orgs that `phi ARCHITECT`_ manages:

`GEOMETOR`_
-----------

*Exploring the architecture of all that is*

- `GitHub <https://github.com/geometor>`_

`HARMONIC resonance`_
---------------------

*Tools to vibrate pixels and speakers*

- `GitHub <https://github.com/harmonic-resonance>`_

.. _`phi ARCHITECT`: https://github.com/phiarchitect
.. _`GEOMETOR`: https://geometor.com/
.. _`HARMONIC resonance`: https://harmonic-resonance.github.io
.. _`website`: https://photon-platform.github.io/
.. _`GitHub organization`: https://github.com/photon-platform
.. _`PHOTON platform`: https://github.com/photon-platform

