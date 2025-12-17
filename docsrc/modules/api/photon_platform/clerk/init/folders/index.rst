photon_platform.clerk.init.folders
==================================

.. py:module:: photon_platform.clerk.init.folders


Attributes
----------

.. autoapisummary::

   photon_platform.clerk.init.folders.base_folder


Functions
---------

.. autoapisummary::

   photon_platform.clerk.init.folders.get_base_project_folder
   photon_platform.clerk.init.folders.list_organization_folders


Module Contents
---------------

.. py:function:: get_base_project_folder() -> pathlib.Path

   Retrieve the base project folder from an environment variable or default to '~/PROJECTS'.

   Returns:
   - Path: A pathlib.Path object representing the base project folder.


.. py:function:: list_organization_folders(base_folder_path: str) -> list[str]

   List the GitHub organization folders present in the base project folder.

   Parameters:
   - base_folder_path (Path): A pathlib.Path object representing the base project folder.

   Returns:
   - list[str]: A list of folder names representing GitHub organizations.


.. py:data:: base_folder

