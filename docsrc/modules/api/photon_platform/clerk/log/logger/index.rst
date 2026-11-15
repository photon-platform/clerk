photon_platform.clerk.log.logger
================================

.. py:module:: photon_platform.clerk.log.logger

.. autoapi-nested-parse::

   PHOTON chronological Sphinx log entry generator.



Attributes
----------

.. autoapisummary::

   photon_platform.clerk.log.logger.LOG_TEMPLATE


Functions
---------

.. autoapisummary::

   photon_platform.clerk.log.logger.create_log_entry


Module Contents
---------------

.. py:data:: LOG_TEMPLATE
   :value: 'log.rst.j2'


.. py:function:: create_log_entry(project_root: pathlib.Path | str, title: str, excerpt: str = '', tags: str | collections.abc.Iterable[str] | None = None, category: str = '', image: str = '', author: str = 'phi ARCHITECT') -> str

   Create a timestamped RST log entry in ``<project_root>/docsrc/log/``.

   :param project_root: Root directory of the target repository.
   :param title: Heading title for the log entry.
   :param excerpt: Short introductory body or summary text.
   :param tags: Comma-separated tag string or iterable of tag strings.
   :param category: Optional log category string.
   :param image: Optional relative image path.
   :param author: Author credit recorded in the ``:author:`` field list.

   :returns: Filesystem path string to the generated ``index.rst`` log file.


