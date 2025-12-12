changelog
=========

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

0.1.0 
-----
*2023-11-15*

**fixed**

.. + Fixed bug in data processing (`#42 <https://github.com/example/repo/issues/42>`_)
.. + Improved error handling in API calls

**added**

.. + Fixed bug in data processing (`#42 <https://github.com/example/repo/issues/42>`_)
.. + Improved error handling in API calls

**changed**

.. + Fixed bug in data processing (`#42 <https://github.com/example/repo/issues/42>`_)
.. + Improved error handling in API calls
