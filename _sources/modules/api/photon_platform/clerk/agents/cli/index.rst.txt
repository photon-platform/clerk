photon_platform.clerk.agents.cli
================================

.. py:module:: photon_platform.clerk.agents.cli

.. autoapi-nested-parse::

   Click CLI commands for `clerk agents` (`status` and `sync`).



Functions
---------

.. autoapisummary::

   photon_platform.clerk.agents.cli.agents
   photon_platform.clerk.agents.cli.status_cmd
   photon_platform.clerk.agents.cli.sync_cmd


Module Contents
---------------

.. py:function:: agents() -> None

   Manage canonical agent definitions, skills, and workspace/global symlinks.


.. py:function:: status_cmd(scope: str, projects_dir: pathlib.Path | None, global_config_dir: pathlib.Path | None, as_json: bool, strict: bool) -> None

   Inspect canonical skills and subagent symlinks across workspaces and global config.


.. py:function:: sync_cmd(scope: str, projects_dir: pathlib.Path | None, global_config_dir: pathlib.Path | None, dry_run: bool, keep_copies: bool, prune: bool, as_json: bool) -> None

   Synchronize workspace `.agents/` and `~/.gemini/config/` symlinks to git repos.


