changelog
=========

0.1.1
-----
*2025-12-19*

**added**

.. + Added ``clerk navigator`` command for TUI-based project navigation.
.. + Implemented Miller Column navigation for exploring organizations and repositories.
.. + Added Context Dashboard with "Project Stats" and "Intelligent Previews".
.. + Added Universal Navigation (up to system root) and smart shortcuts (``s``, ``d``, ``t``).
.. + Implemented shell integration to change directory on exit.

0.1.0
-----
*2025-12-17*

**added**

.. + Introduced ``track`` module for scanning and reporting on project tasks/todos.
.. + Supported Rich, Markdown, JSON, and list output formats for ``track``.

**refactored**

.. + Reorganized project documentation structure, moving ``todos.rst`` to ``docsrc/todos/index.rst``.
.. + Updated ``clerk init`` templates to support the new documentation structure.
.. + Refined ``log`` command templates.

0.0.11
------
*2025-12-12*

**refactored**

.. + Integrated ``rollup`` and ``status`` commands into ``clerk curate``.
.. + Removed unused ``openai`` dependency.
.. + Cleaned up ``pyproject.toml`` dependencies.

0.0.10
------
*2025-12-12*

**refactored**

.. + Renamed top-level modules to action-oriented verbs: ``init``, ``build``, ``curate``, ``log``.
.. + Simplified ``build`` command names (e.g. ``module`` instead of ``create-module``).
.. + Moved ``rollup`` and ``status_diff`` into ``curate`` module.

0.0.9
-----
*2025-12-12*

**changed**

.. + Updated `README.rst` to accurately document CLI arguments and remove legacy roadmap.
.. + Improved `gather` command documentation in `README.rst`.


0.0.8
-----
*2025-12-11*

**added**

.. + Added comprehensive usage documentation for `curator`, `gather`, `logger`, `modulator`, and `progenitor`.
.. + Improved documentation structure and navigation in `docsrc`.

0.0.7
-----
*2025-12-11*

**refactored**

.. + Refactored `clerk` CLI into context-aware sub-apps (`progenitor`, `modulator`, `curator`, `gather`, `logger`).
.. + Removed legacy TUI applications in favor of a unified Click-based CLI.
.. + Implemented `Context` class for automatic situational awareness and path detection.
.. + Cleaned up redundant entry points and files.

0.0.6
-----
*2025-11-06*

**refactored**

.. + Made `progenitor` command context-aware, inferring GitHub ID and package namespace from the current path.
.. + Moved `git_init` functionality from `progenitor` to `curator` under a new `init` command.
.. + Fixed various import errors related to the recent refactoring of modules under `clerk`.

0.0.5
-----
*2025-11-05*

**refactored**

.. + Consolidated summarizer and other web scraping functions into a unified `gather` module.
.. + Reorganized `curator` module to use standalone, action-oriented functions.
.. + Updated the main `clerk` CLI to reflect the new module structure and commands.
.. + Removed the `projector` module as its functionality is covered by other tools.

0.0.4
-----
*2025-11-05*

**added**

.. + Integrated progenitor, modulator, curator, logger, and summarizer into clerk as subcommands.
.. + Converted the application from a Textual app to a Click-based CLI.

0.0.3
-----
*2025-11-04*

**changed**

.. + Updated ``GEMINI.md`` with integration details.

0.0.2
-----
*2025-11-04*

**added**

.. + ``rollup`` script to automate the release process.
.. + ``status_diff`` script to show git status and diff since branching from main.
