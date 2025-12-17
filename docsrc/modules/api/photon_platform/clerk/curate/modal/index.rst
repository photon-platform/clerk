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


   A screen with bindings that take precedence over the App's key bindings.

   The default styling of a modal screen will dim the screen underneath.


   .. py:method:: compose() -> textual.app.ComposeResult

      Called by Textual to create child widgets.

      This method is called when a widget is mounted or by setting `recompose=True` when
      calling [`refresh()`][textual.widget.Widget.refresh].

      Note that you don't typically need to explicitly call this method.

      .. rubric:: Example

      ```python
      def compose(self) -> ComposeResult:
          yield Header()
          yield Label("Press the button below:")
          yield Button()
          yield Footer()
      ```



   .. py:method:: on_button_pressed(event: textual.widgets.Button.Pressed) -> None


.. py:class:: ErrorScreen(errors: list)

   Bases: :py:obj:`textual.screen.ModalScreen`


   A screen with bindings that take precedence over the App's key bindings.

   The default styling of a modal screen will dim the screen underneath.


   .. py:method:: compose() -> textual.app.ComposeResult

      Called by Textual to create child widgets.

      This method is called when a widget is mounted or by setting `recompose=True` when
      calling [`refresh()`][textual.widget.Widget.refresh].

      Note that you don't typically need to explicitly call this method.

      .. rubric:: Example

      ```python
      def compose(self) -> ComposeResult:
          yield Header()
          yield Label("Press the button below:")
          yield Button()
          yield Footer()
      ```



   .. py:method:: on_button_pressed(event: textual.widgets.Button.Pressed) -> None


