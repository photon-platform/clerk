CLERK: Command-Line Executor for Rapid Knowledge
================================================

The CLERK project is a pivotal component of the `PHOTON platform`_, a suite of
tools committed to gathering, processing, and publishing knowledge. Inspired by
Douglas Engelbart's vision of the computer as a "clerk" in his seminal paper,
`Augmenting Human Intellect`_, CLERK is a powerful command-line tool, designed
to provide situational awareness and context-sensitive operations based on the
current working directory (CWD) and the information it contains.

Here are the roles of CLERK, each fulfilling a unique function within the
knowledge management process:

- `progenitor`: Sparks life into Python projects.
- `modulator`: Shapes Python modules and packages.
- `curator`: Organizes git/archive management.
- `logger`: Creates log entries.
- `gather`: Downloads and organizes information from the web. It can handle various sources like URLs, GitHub repositories, arXiv papers, and YouTube videos.

Usage
-----

Here is a summary of the CLERK CLI interface:

Top-Level Commands
~~~~~~~~~~~~~~~~~~

- `clerk gather`: Gathers content from various sources.
- `clerk logger`: Creates a new log entry.
- `clerk progenitor`: Creates a new Python project.
- `clerk modulator`: Shapes Python modules and packages.
- `clerk curator`: Organizes git/archive management.

`gather` Commands
~~~~~~~~~~~~~~~~~

- `clerk gather url <url_string>`: Gathers content from a URL. It intelligently handles sources like Wikipedia, arXiv, YouTube, GitHub, and general web pages.
- `clerk gather repo <repo_string>`: Gathers information about a GitHub repository (e.g., `owner/repo`).

`logger` Command
~~~~~~~~~~~~~~~~

- `clerk logger`: This command takes no arguments and opens an interactive prompt to create a new log entry.

`progenitor` Command
~~~~~~~~~~~~~~~~~~~~

- `clerk progenitor`: Creates a new Python project. It prompts for the following information:
    - `--github-id`: Your GitHub username or organization.
    - `--package-namespace`: The namespace for the package.
    - `--github-repo-id`: The name of the GitHub repository.
    - `--package-name`: The name of the Python package.
    - `--author`: The name of the author.
    - `--description`: A short description of the project.
    - `--path`: The path to create the project in.

`modulator` Commands
~~~~~~~~~~~~~~~~~~~~

- `clerk modulator create-module`: Creates a new Python module.
- `clerk modulator create-submodule`: Creates a new Python submodule.
- `clerk modulator create-class`: Creates a new Python class.
- `clerk modulator create-function`: Creates a new Python function.
- `clerk modulator create-class-method`: Creates a new Python class method.

(Each `modulator` command prompts for necessary information like project path, namespace, module name, etc.)

`curator` Commands
~~~~~~~~~~~~~~~~~~

- `clerk curator branches`: Lists the branches in the repository.
- `clerk curator create-release-branch`: Creates a new release branch.
- `clerk curator merge-to-main`: Merges a branch to main.
- `clerk curator create-tag`: Creates a new tag.

(Each `curator` command can take a `--repo-path` and will prompt for other necessary information.)


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
