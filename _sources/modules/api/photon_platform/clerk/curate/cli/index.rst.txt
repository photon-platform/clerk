photon_platform.clerk.curate.cli
================================

.. py:module:: photon_platform.clerk.curate.cli


Functions
---------

.. autoapisummary::

   photon_platform.clerk.curate.cli.curate
   photon_platform.clerk.curate.cli.branches
   photon_platform.clerk.curate.cli.create_release_branch
   photon_platform.clerk.curate.cli.merge_to_main
   photon_platform.clerk.curate.cli.create_tag
   photon_platform.clerk.curate.cli.init_repo
   photon_platform.clerk.curate.cli.rollup
   photon_platform.clerk.curate.cli.status


Module Contents
---------------

.. py:function:: curate()

   Organizes git/archive management.


.. py:function:: branches(ctx, repo_path)

   Lists the branches in the repository.


.. py:function:: create_release_branch(ctx, repo_path, release_version, description)

   Creates a new release branch.


.. py:function:: merge_to_main(ctx, repo_path, branch_name, commit_message)

   Merges a branch to main.


.. py:function:: create_tag(ctx, repo_path, tag_name, message)

   Creates a new tag.


.. py:function:: init_repo()

   Initializes a new git repository.


.. py:function:: rollup()

   Automates the release process.


.. py:function:: status()

   Shows git status and diff.


