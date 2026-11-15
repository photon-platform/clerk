photon_platform.clerk.build.modulator
=====================================

.. py:module:: photon_platform.clerk.build.modulator

.. autoapi-nested-parse::

   Python namespace package and module scaffolder for Clerk.



Classes
-------

.. autoapisummary::

   photon_platform.clerk.build.modulator.Modulator


Module Contents
---------------

.. py:class:: Modulator(project_path: pathlib.Path, namespace: str)

   Generate Python 3.13 namespace modules and CLI entry points.


   .. py:attribute:: project_path


   .. py:attribute:: namespace


   .. py:attribute:: env


   .. py:method:: create_module(module_name: str, *, description: str | None = None, cli_name: str | None = None, author: str = 'phi ARCHITECT', archetype: str = 'code') -> pathlib.Path

      Scaffold ``src/<namespace>/<module_name>/`` with ``__init__``, ``app``, and ``__main__``.

      :param module_name: Python module or dotted submodule identifier.
      :param description: Human-readable package summary for module docstrings and ``--help``.
      :param cli_name: Console-script display name (defaults to ``module_name``).
      :param author: Author name for metadata.
      :param archetype: Repository archetype (``"code"``, ``"codex"``, or ``"catalog"``).

      :returns: Directory path of the created Python package.



   .. py:method:: create_submodule(module_name: str, submodule_name: str) -> pathlib.Path

      Create a nested submodule under ``module_name``.

      :param module_name: Parent package name.
      :param submodule_name: Child submodule name.

      :returns: Directory path of the created submodule.



   .. py:method:: create_class(module_name: str, class_name: str) -> pathlib.Path

      Create a standalone Python 3.13 class module stub.

      :param module_name: Target package name under ``src/<namespace>/``.
      :param class_name: Class name to scaffold.

      :returns: Filesystem path of the created class module.



   .. py:method:: create_function(module_name: str, function_name: str, args: str, return_type: str) -> pathlib.Path

      Append a typed function stub to ``<module_name>.py``.

      :param module_name: Target package name under ``src/<namespace>/``.
      :param function_name: Function identifier.
      :param args: Parameter signature string.
      :param return_type: Return type annotation string.

      :returns: Filesystem path of the updated module file.



   .. py:method:: create_class_method(module_name: str, class_name: str, method_name: str, args: str, return_type: str) -> pathlib.Path

      Append a typed method stub to an existing class file.

      :param module_name: Target package name under ``src/<namespace>/``.
      :param class_name: Target class module name.
      :param method_name: Method identifier.
      :param args: Parameter signature string (excluding ``self``).
      :param return_type: Return type annotation string.

      :returns: Filesystem path of the updated class file.



