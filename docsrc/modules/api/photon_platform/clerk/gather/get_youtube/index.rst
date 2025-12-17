photon_platform.clerk.gather.get_youtube
========================================

.. py:module:: photon_platform.clerk.gather.get_youtube

.. autoapi-nested-parse::

   YouTube video utility - creates RST documentation with video metadata and embedded player



Functions
---------

.. autoapisummary::

   photon_platform.clerk.gather.get_youtube.run_yt_command
   photon_platform.clerk.gather.get_youtube.create_include_files
   photon_platform.clerk.gather.get_youtube.format_rst
   photon_platform.clerk.gather.get_youtube.action_gather_youtube


Module Contents
---------------

.. py:function:: run_yt_command(video_id: str, option: str, output_file: pathlib.Path = None) -> dict

   Run yt command and return parsed output or save to file.


.. py:function:: create_include_files(video_dir: pathlib.Path)

   Create include files for notes and analysis.


.. py:function:: format_rst(data: dict) -> str

   Format video data as RST document.


.. py:function:: action_gather_youtube(video_id: str, output_dir: str = '.') -> pathlib.Path

   Save video metadata as RST.


