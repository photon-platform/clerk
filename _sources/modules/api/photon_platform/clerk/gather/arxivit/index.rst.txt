photon_platform.clerk.gather.arxivit
====================================

.. py:module:: photon_platform.clerk.gather.arxivit

.. autoapi-nested-parse::

   ArXiv reference utility - downloads papers and creates RST documentation



Functions
---------

.. autoapisummary::

   photon_platform.clerk.gather.arxivit.get_paper_data
   photon_platform.clerk.gather.arxivit.create_include_files
   photon_platform.clerk.gather.arxivit.format_rst
   photon_platform.clerk.gather.arxivit.action_gather_arxiv


Module Contents
---------------

.. py:function:: get_paper_data(paper_id: str) -> dict

   Fetch paper metadata from arXiv.


.. py:function:: create_include_files(paper_dir: pathlib.Path)

   Create include files: premise, outline, quotes, and notes.


.. py:function:: format_rst(data: dict) -> str

   Format paper data as RST document.


.. py:function:: action_gather_arxiv(paper_id: str, output_dir: str = '.') -> tuple[pathlib.Path, pathlib.Path]

   Save paper metadata as RST and download PDF.


