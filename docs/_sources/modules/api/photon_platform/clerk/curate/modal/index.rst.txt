photon_platform.clerk.curate.modal
==================================

.. py:module:: photon_platform.clerk.curate.modal


Classes
-------

.. autoapisummary::

   photon_platform.clerk.curate.modal.AlertScreen
   photon_platform.clerk.curate.modal.ErrorScreen


Module Contents
---------------

.. py:class:: AlertScreen(message: str)

   Bases: :py:obj:`textual.screen.ModalScreen`


   .. py:method:: compose() -> textual.app.ComposeResult


   .. py:method:: on_button_pressed(event: textual.widgets.Button.Pressed) -> None


.. py:class:: ErrorScreen(errors: list)

   Bases: :py:obj:`textual.screen.ModalScreen`


   .. py:method:: compose() -> textual.app.ComposeResult


   .. py:method:: on_button_pressed(event: textual.widgets.Button.Pressed) -> None


