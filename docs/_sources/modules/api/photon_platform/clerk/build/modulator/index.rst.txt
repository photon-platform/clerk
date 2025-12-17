photon_platform.clerk.build.modulator
=====================================

.. py:module:: photon_platform.clerk.build.modulator


Classes
-------

.. autoapisummary::

   photon_platform.clerk.build.modulator.Modulator


Module Contents
---------------

.. py:class:: Modulator(project_path: pathlib.Path, namespace: str)

   .. py:attribute:: project_path


   .. py:attribute:: namespace


   .. py:attribute:: env


   .. py:method:: create_module(module_name: str) -> None


   .. py:method:: create_submodule(module_name: str, submodule_name: str) -> None


   .. py:method:: create_class(module_name: str, class_name: str) -> None


   .. py:method:: create_function(module_name: str, function_name: str, args: str, return_type: str) -> None


   .. py:method:: create_class_method(module_name: str, class_name: str, method_name: str, args: str, return_type: str) -> None


