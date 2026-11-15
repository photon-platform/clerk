photon_platform.clerk.init.progenitor
=====================================

.. py:module:: photon_platform.clerk.init.progenitor

.. autoapi-nested-parse::

   Repository scaffolding engine supporting code, codex, and catalog archetypes.



Attributes
----------

.. autoapisummary::

   photon_platform.clerk.init.progenitor.ARCHETYPES


Functions
---------

.. autoapisummary::

   photon_platform.clerk.init.progenitor.create_project


Module Contents
---------------

.. py:data:: ARCHETYPES
   :type:  tuple[str, ...]
   :value: ('code', 'codex', 'catalog')


.. py:function:: create_project(github_id: str, package_namespace: str, github_repo_id: str, package_name: str, author: str, description: str | None, path: str | pathlib.Path, *, archetype: str = 'code', edition_slug: str | None = None, book_title: str | None = None, book_author: str | None = None, git_init: bool = False) -> pathlib.Path | None

   Create a new Python 3.13 project repository from archetype templates.

   :param github_id: GitHub organization or account slug (e.g. ``"geometor"``).
   :param package_namespace: Top-level Python namespace package (e.g. ``"geometor"``).
   :param github_repo_id: Repository folder and GitHub slug (preserves hyphens).
   :param package_name: Python package name under ``src/<package_namespace>/``.
   :param author: Maintainer / copyright holder name.
   :param description: One-line repository summary (auto-populated if ``None`` or empty).
   :param path: Parent directory in which ``<github_repo_id>/`` will be created.
   :param archetype: One of ``"code"``, ``"codex"``, or ``"catalog"``.
   :param edition_slug: Primary codex edition directory slug (defaults to ``package_name``).
   :param book_title: Optional scholarly treatise or catalog display title.
   :param book_author: Optional primary historical or curated author attribution.
   :param git_init: If ``True``, initialize a git repository on branch ``main``.

   :returns: Created ``project_path`` :class:`~pathlib.Path`, or ``None`` if target already exists.

   :raises ValueError: If ``archetype`` is not one of :data:`ARCHETYPES`.


