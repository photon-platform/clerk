photon_platform.clerk.curate.git_reset
======================================

.. py:module:: photon_platform.clerk.curate.git_reset


Functions
---------

.. autoapisummary::

   photon_platform.clerk.curate.git_reset.get_remote_origin_url
   photon_platform.clerk.curate.git_reset.reset_git_repo
   photon_platform.clerk.curate.git_reset.main


Module Contents
---------------

.. py:function:: get_remote_origin_url(repo_path)

   Gets the URL of the 'origin' remote for the Git repository.

   :param repo_path: The path to the Git repository.
   :type repo_path: str

   :returns: The URL of the 'origin' remote, or None if not found or an error occurs.
   :rtype: str or None


.. py:function:: reset_git_repo(repo_path='.', force_push=False)

   Resets the Git repository at the specified path to a 'main' branch
   and optionally force pushes.

   This involves:
   1. Finding the remote origin URL.
   2. Asking for confirmation.
   3. Deleting the .git directory.
   4. Re-initializing the repository with the 'main' branch.
   5. Adding the remote origin back (if found).
   6. Staging all files.
   7. Creating an initial commit.
   8. Optionally force-pushing to the 'main' branch on remote origin.

   :param repo_path: The path to the Git repository (default: current directory).
   :type repo_path: str
   :param force_push: Whether to force push to remote 'main' branch after reset (default: False).
   :type force_push: bool


.. py:function:: main()

   CLI entry point for `git‑reset`.  Parses arguments and
   calls `reset_git_repo`.


