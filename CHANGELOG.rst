changelog
=========

0.2.2
-----
*2026-11-16*

**changed**

- Upgrade ``clerk init`` templates (``progenitor.py``, ``README.rst.j2``, ``docsrc/index.rst.j2``, ``docsrc/intro.rst.j2``, ``action.yml.j2``) to the unified **Semantic Digital Archive** standard: ``GEOMETOR • <repo>`` storefront mastheads with top-of-page **Visit the Online Archive** CTA, ``•``-delimited ``semantic digital archive`` descriptions and topic pill defaults (``books``, ``catalogs``, ``people``, ``modules``), harmonized ``semantic digital archive • ...`` Homepage overlines and opening narratives, and ``geometor/model.git`` CI wiring for catalog scaffolds.

0.2.1
-----
*2026-11-15*

**changed**

- Align ``clerk init`` templates (``progenitor.py``, ``conf.py.j2``, ``index.rst.j2``, ``intro.rst.j2``, ``codex/index.rst.j2``, ``catalog/index.rst.j2``, ``about/index.rst.j2``) with the Digital Scriptorium Book Codex contract: human-first ``A–Z`` ``site_title`` metadata, *"the works of / ``<FULL NAME>``"* Author Home Pages with ``.. collection::``, clean Book Title Pages (moving ``structure_map.json`` / provenance details to ``About``), standardized 3-part GEOMETOR Mission in ``About``, and automatic ``1200x630`` ``_static/social/`` banner generation.

0.2.0
-----
*2026-11-15*

**added**

- Add ``--type code | codex | catalog`` repository archetypes to ``clerk init`` along with ``--edition``, ``--title``, ``--book-author``, ``--org``, and ``--git/--no-git`` options.
- Generate ``GEMINI.md``, ``ROADMAP.md``, baseline ``tests/test_<package>.py``, ``:layout: book`` codex/catalog tracks, and ``CatalogEntrySpec`` / ``assert_no_floats`` helpers out-of-the-box.

**fixed**

- Enforce Jinja2 ``StrictUndefined`` across ``progenitor``, ``Modulator``, and ``logger`` templates, resolving undefined template variables, hyphenated package identifier collisions, broken ``Modulator`` class-import stubs, offline ``intersphinx_mapping`` timeouts, and ``clerk log`` tag/date rendering.
- Fix ``determine_context`` org detection when invoked directly at ``~/PROJECTS/<org>`` containing an org-level ``pyproject.toml`` workspace manifest.

0.1.4
-----
*2026-11-15*

**added**

- Provision canonical ``geometor`` and ``photon-platform`` ``logo.png`` and ``favicon.ico`` brand assets in ``docsrc/_static/`` during ``clerk init`` project scaffolding, and add ``clerk``'s own ``docsrc/_static/logo.png`` and ``favicon.ico``.

0.1.3
-----
*2026-11-13*

**changed**

- Update canonical ``clerk`` agent model to ``flash``.

0.1.2
-----
*2026-11-12*

**added**

- Added canonical ``clerk-branch`` and ``clerk-rollup`` skills and ``clerk`` subagent definition.
- Added ``clerk agents status`` and ``clerk agents sync`` CLI commands and symlink registry for PHOTON and GEOMETOR workspaces.

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
