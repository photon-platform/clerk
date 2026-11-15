photon_platform.clerk.navigator.screens.file_screen
===================================================

.. py:module:: photon_platform.clerk.navigator.screens.file_screen

.. autoapi-nested-parse::

   Screen for file preview and agent actions.



Classes
-------

.. autoapisummary::

   photon_platform.clerk.navigator.screens.file_screen.FileScreen


Module Contents
---------------

.. py:class:: FileScreen(file_path: pathlib.Path)

   Bases: :py:obj:`textual.screen.Screen`


   Provides a preview of a file and actions for coordination.


   .. py:attribute:: BINDINGS
      :value: [('h', 'app.pop_screen', 'Back'), ('j', 'scroll_down', 'Down'), ('k', 'scroll_up', 'Up'), ('e',...



   .. py:attribute:: file_path


   .. py:method:: compose() -> textual.app.ComposeResult


   .. py:method:: on_mount() -> None


   .. py:method:: action_scroll_up() -> None


   .. py:method:: action_scroll_down() -> None


   .. py:method:: update_preview() -> None


   .. py:method:: action_edit_file() -> None


   .. py:method:: action_export_for_agent() -> None


