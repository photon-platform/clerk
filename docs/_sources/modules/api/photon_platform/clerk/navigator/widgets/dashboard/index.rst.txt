photon_platform.clerk.navigator.widgets.dashboard
=================================================

.. py:module:: photon_platform.clerk.navigator.widgets.dashboard


Classes
-------

.. autoapisummary::

   photon_platform.clerk.navigator.widgets.dashboard.DashboardPanel


Module Contents
---------------

.. py:class:: DashboardPanel

   Bases: :py:obj:`textual.widgets.Static`


   A panel for situational awareness showing project or org stats.


   .. py:method:: update_repo_stats(path: pathlib.Path)

      Update the panel with repository-specific statistics.



   .. py:method:: find_project_root(path: pathlib.Path) -> Optional[pathlib.Path]

      Climb up from path to find a .git or pyproject.toml.



   .. py:method:: update_org_stats(org_path: pathlib.Path)

      Update the panel with organization-level awareness.



   .. py:method:: gather_repo_stats(repo_path: pathlib.Path) -> dict


