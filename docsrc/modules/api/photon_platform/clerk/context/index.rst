photon_platform.clerk.context
=============================

.. py:module:: photon_platform.clerk.context

.. autoapi-nested-parse::

   Context detection for Clerk across PHOTON and GEOMETOR workspaces.



Classes
-------

.. autoapisummary::

   photon_platform.clerk.context.Context


Functions
---------

.. autoapisummary::

   photon_platform.clerk.context.determine_context


Module Contents
---------------

.. py:class:: Context

   Resolved filesystem, organization, and git context for a Clerk invocation.


   .. py:attribute:: path
      :type:  pathlib.Path


   .. py:attribute:: org_name
      :type:  str | None
      :value: None



   .. py:attribute:: repo_name
      :type:  str | None
      :value: None



   .. py:attribute:: project_root
      :type:  pathlib.Path | None
      :value: None



   .. py:attribute:: git_branch
      :type:  str | None
      :value: None



   .. py:attribute:: is_dirty
      :type:  bool
      :value: False



   .. py:property:: is_project
      :type: bool


      Return whether ``path`` sits inside a detected repository root.


   .. py:property:: is_src
      :type: bool


      Return whether ``path`` is inside a ``src`` subtree.


   .. py:property:: is_docs
      :type: bool


      Return whether ``path`` is inside ``docs`` or ``docsrc``.


   .. py:property:: is_tests
      :type: bool


      Return whether ``path`` is inside a ``tests`` subtree.


   .. py:method:: export_for_agent() -> str

      Export the current context as a structured string for agents.

      :returns: Newline-delimited key/value summary of the detected context.



.. py:function:: determine_context(path: pathlib.Path) -> Context

   Determine the workspace/repository context based on ``path``.

   Assumes a workspace hierarchy of ``~/PROJECTS/<org>/<repo>`` or git/pyproject
   markers. When ``path`` points directly to ``~/PROJECTS/<org>`` (even if an
   org-level ``pyproject.toml`` workspace manifest is present), ``org_name`` is
   resolved to ``<org>`` rather than misclassifying ``PROJECTS`` as an org.

   :param path: Directory path to inspect.

   :returns: Populated :class:`Context` instance.


