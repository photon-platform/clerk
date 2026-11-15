photon_platform.clerk.context
=============================

.. py:module:: photon_platform.clerk.context

.. autoapi-nested-parse::

   Context detection for Clerk.



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

   .. py:attribute:: path
      :type:  pathlib.Path


   .. py:attribute:: org_name
      :type:  Optional[str]
      :value: None



   .. py:attribute:: repo_name
      :type:  Optional[str]
      :value: None



   .. py:attribute:: project_root
      :type:  Optional[pathlib.Path]
      :value: None



   .. py:attribute:: git_branch
      :type:  Optional[str]
      :value: None



   .. py:attribute:: is_dirty
      :type:  bool
      :value: False



   .. py:property:: is_project
      :type: bool



   .. py:property:: is_src
      :type: bool



   .. py:property:: is_docs
      :type: bool



   .. py:property:: is_tests
      :type: bool



   .. py:method:: export_for_agent() -> str

      Export the current context as a structured string for agents.



.. py:function:: determine_context(path: pathlib.Path) -> Context

   Determine the context based on the current path.
   Assumes a structure of ~/PROJECTS/<org>/<repo> or git/pyproject markers.


