photon_platform.clerk.log.lister
================================

.. py:module:: photon_platform.clerk.log.lister

.. autoapi-nested-parse::

   PHOTON lister



Attributes
----------

.. autoapisummary::

   photon_platform.clerk.log.lister.LOG_TEMPLATE
   photon_platform.clerk.log.lister.app


Classes
-------

.. autoapisummary::

   photon_platform.clerk.log.lister.Lister


Module Contents
---------------

.. py:data:: LOG_TEMPLATE
   :value: 'log.rst.j2'


.. py:class:: Lister

   Bases: :py:obj:`textual.app.App`


   .. py:attribute:: CSS_PATH
      :value: 'logger.css'



   .. py:attribute:: TITLE
      :value: 'PHOTON • log lister'



   .. py:attribute:: BINDINGS
      :value: [('ctrl+s', 'save', 'save'), ('ctrl+p', 'screenshot', 'screenshot'), ('ctrl+q', 'quit', 'quit')]



   .. py:method:: compose() -> textual.app.ComposeResult


   .. py:method:: on_button_pressed(event: textual.widgets.Button.Pressed) -> None

      Event handler called when a button is pressed.



   .. py:method:: action_save()


   .. py:method:: action_screenshot(path: str = './') -> None

      Save an SVG "screenshot". This action will save an SVG file containing the current contents of the screen.

      :param filename: Filename of screenshot, or None to auto-generate. Defaults to None.
      :type filename: str | None, optional
      :param path: Path to directory. Defaults to "./".
      :type path: str, optional



.. py:data:: app

