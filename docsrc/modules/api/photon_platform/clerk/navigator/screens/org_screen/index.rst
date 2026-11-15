photon_platform.clerk.navigator.screens.org_screen
==================================================

.. py:module:: photon_platform.clerk.navigator.screens.org_screen

.. autoapi-nested-parse::

   Screen for organization-level navigation.



Classes
-------

.. autoapisummary::

   photon_platform.clerk.navigator.screens.org_screen.OrgScreen


Module Contents
---------------

.. py:class:: OrgScreen(org_path: pathlib.Path)

   Bases: :py:obj:`textual.screen.Screen`


   Lists repositories within an organization.


   .. py:attribute:: BINDINGS
      :value: [('j', 'move_down', 'Down'), ('k', 'move_up', 'Up'), ('l', 'select_repo', 'Select'), ('enter',...



   .. py:attribute:: org_path


   .. py:attribute:: repos
      :value: []



   .. py:method:: compose() -> textual.app.ComposeResult


   .. py:method:: on_mount() -> None
      :async:



   .. py:method:: on_screen_resume() -> None


   .. py:method:: refresh_view() -> None
      :async:


      Refresh the view when view_mode or show_hidden changes.



   .. py:method:: load_repos()
      :async:



   .. py:method:: load_parent_column()


   .. py:method:: on_data_table_row_highlighted(event: textual.widgets.DataTable.RowHighlighted) -> None
      :async:



   .. py:method:: action_move_up() -> None
      :async:



   .. py:method:: action_move_down() -> None
      :async:



   .. py:method:: action_select_repo() -> None
      :async:



   .. py:method:: action_navigate_back() -> None
      :async:



