Track
=====

The ``track`` command is used to scan for and report on todo files across the project workspace. It provides a centralized view of distributed tasks defined in markdown files.

Usage
-----

.. code-block:: bash

    clerk track [OPTIONS] [COMMAND]

By default, running ``clerk track`` produces a **Rich** text report, listing all todos sorted by priority (order) across all projects.

Options
-------

.. option:: --group

    Group the output by project. When this flag is used, todos are listed under their respective project headers, sorted by priority within each project.

    .. code-block:: bash

        clerk track --group

Subcommands
-----------

md
~~

Output the report in Markdown format. This is useful for generating documentation or piping to other tools.

.. code-block:: bash

    clerk track md

json
~~~~

Output the report in JSON format. Use this for programmatic processing of todos.

.. code-block:: bash

    clerk track json

list
~~~~

Output a simple list of todo titles, sorted globally by order.

.. code-block:: bash

    clerk track list

Todo File Format
----------------

The ``track`` command scans for markdown files (``.md``) located in:

*   ``docsrc/todos/`` within any project.
*   ``todos/`` at the organizational or root level.

Each markdown file represents a todo item. Formatting conventions:

*   **Frontmatter**: Use YAML frontmatter to specify metadata, primarily the ``order``.
*   **Title**: The first H1 header (`# Title`) is used as the todo summary.
*   **Content**: Any remaining text is treated as the description/body.

Example ``docsrc/todos/my_task.md``:

.. code-block:: markdown

    ---
    order: 1
    ---

    # My Critical Task

    Detailed description of what needs to be done.
    - Sub-item 1
    - Sub-item 2
