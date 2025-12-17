photon_platform.clerk.gather.repo_rst
=====================================

.. py:module:: photon_platform.clerk.gather.repo_rst

.. autoapi-nested-parse::

   GitHub repository utility - fetches repo info and creates RST documentation



Functions
---------

.. autoapisummary::

   photon_platform.clerk.gather.repo_rst.run_gh_command
   photon_platform.clerk.gather.repo_rst.get_repo_data
   photon_platform.clerk.gather.repo_rst.create_include_files
   photon_platform.clerk.gather.repo_rst.format_rst
   photon_platform.clerk.gather.repo_rst.fetch_and_save_readme
   photon_platform.clerk.gather.repo_rst.action_gather_repo


Module Contents
---------------

.. py:function:: run_gh_command(args: list, fields: str = None) -> dict

   Run GitHub CLI command and return JSON output.


.. py:function:: get_repo_data(repo: str) -> dict

   Fetch repository metadata from GitHub.


.. py:function:: create_include_files(repo_dir: pathlib.Path)

   Create include files for analysis sections.


.. py:function:: format_rst(data: dict, readme_content: str = '') -> str

   Format repository data as RST document.


.. py:function:: fetch_and_save_readme(data: dict, repo_dir: pathlib.Path) -> tuple[bool, str]

   Fetch and save README file, trying MD then RST format.


.. py:function:: action_gather_repo(repo: str, output_dir: str = '.') -> pathlib.Path

   Save repository metadata as RST.


