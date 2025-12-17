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


.. py:class:: Lister(driver_class: Type[textual.driver.Driver] | None = None, css_path: textual._path.CSSPathType | None = None, watch_css: bool = False, ansi_color: bool = False)

   Bases: :py:obj:`textual.app.App`


   The base class for Textual Applications.


   .. py:attribute:: CSS_PATH
      :value: 'logger.css'


      File paths to load CSS from.


   .. py:attribute:: TITLE
      :value: 'PHOTON • log lister'


      A class variable to set the *default* title for the application.

      To update the title while the app is running, you can set the [title][textual.app.App.title] attribute.
      See also [the `Screen.TITLE` attribute][textual.screen.Screen.TITLE].


   .. py:attribute:: BINDINGS
      :value: [('ctrl+s', 'save', 'save'), ('ctrl+p', 'screenshot', 'screenshot'), ('ctrl+q', 'quit', 'quit')]


      The default key bindings.


   .. py:method:: compose() -> textual.app.ComposeResult

      Yield child widgets for a container.

      This method should be implemented in a subclass.



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

