:order: 4

gather
======

The ``gather`` command scrapes and consolidates content from URLs and repositories.

Context Awareness
-----------------

Gather operations are currently **Context Agnostic**. They operate on the explicit URL or repository string provided and do not infer context from the local directory.

Usage
-----

.. click:: photon_platform.clerk.gather.cli:gather
   :prog: clerk gather
   :nested: full
