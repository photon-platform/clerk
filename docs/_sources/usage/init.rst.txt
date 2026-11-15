:order: 1

====
init
====

The ``clerk init`` command scaffolds new Python 3.13 repositories across **PHOTON** and **GEOMETOR** workspaces with out-of-the-box ``pytest``, ``ruff``, and ``publish build`` compliance.

Repository Archetypes (``--type``)
----------------------------------

- ``code`` *(default)* — Standard Python 3.13 namespace package, typed CLI, baseline test suite, and Sphinx Foundation documentation.
- ``codex`` — Digital Scriptorium treatise edition with ``:layout: book`` under ``docsrc/<edition>/``, ``resources/<edition>/structure_map.json``, and scholarly apparatus (``persons.json``, ``citations.json``, ``glossary.json``).
- ``catalog`` — Exact symbolic mathematical catalog and cross-corpus concordance with ``:layout: book`` under ``docsrc/catalog/``, ``CatalogEntrySpec`` + ``assert_no_floats`` validator, ``resources/catalog_manifest.json``, and ``resources/concordance.json``.

Examples
--------

.. code-block:: bash

   clerk init my-tool
   clerk init piero --type codex --edition quinque_corporibus --title "Libellus de Quinque Corporibus Regularibus" --book-author "Piero della Francesca"
   clerk init posamentier --type catalog --title "The Glorious Golden Ratio" --book-author "Alfred S. Posamentier & Ingmar Lehmann"

CLI Options
-----------

.. code-block:: text

   Usage: clerk init [OPTIONS] PROJECT_NAME

   Options:
     -d, --description TEXT              Short repository summary.
     -t, --type [code|codex|catalog]     Repository archetype [default: code]
     --edition TEXT                      Primary edition slug for --type codex.
     --title TEXT                        Display title for codex or catalog.
     --book-author TEXT                  Historical/source author attribution.
     --org TEXT                          Override detected GitHub organization.
     --git / --no-git                    Initialize git repository on branch main [default: git]
     --help                              Show this message and exit.
