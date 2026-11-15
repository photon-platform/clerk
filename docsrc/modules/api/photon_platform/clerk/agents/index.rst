photon_platform.clerk.agents
============================

.. py:module:: photon_platform.clerk.agents

.. autoapi-nested-parse::

   Agent skills and subagent definition discovery and symlink synchronization.



Submodules
----------

.. toctree::
   :maxdepth: 1

   /modules/api/photon_platform/clerk/agents/cli/index
   /modules/api/photon_platform/clerk/agents/registry/index


Attributes
----------

.. autoapisummary::

   photon_platform.clerk.agents.DEFAULT_TOOL_REPO_SPECS


Classes
-------

.. autoapisummary::

   photon_platform.clerk.agents.CustomizationItem
   photon_platform.clerk.agents.LinkCheck
   photon_platform.clerk.agents.StatusReport
   photon_platform.clerk.agents.SyncAction
   photon_platform.clerk.agents.SyncReport
   photon_platform.clerk.agents.TargetRoot
   photon_platform.clerk.agents.ToolRepoSpec


Functions
---------

.. autoapisummary::

   photon_platform.clerk.agents.agents
   photon_platform.clerk.agents.build_target_roots
   photon_platform.clerk.agents.check_status
   photon_platform.clerk.agents.discover_customizations
   photon_platform.clerk.agents.sync_links


Package Contents
----------------

.. py:function:: agents() -> None

   Manage canonical agent definitions, skills, and workspace/global symlinks.


.. py:data:: DEFAULT_TOOL_REPO_SPECS
   :type:  tuple[ToolRepoSpec, ...]

.. py:class:: CustomizationItem

   A canonical skill directory or subagent Markdown definition.


   .. py:attribute:: kind
      :type:  CustomizationKind


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: repo
      :type:  str


   .. py:attribute:: source_path
      :type:  pathlib.Path


   .. py:attribute:: source_exists
      :type:  bool


   .. py:method:: to_dict() -> dict[str, Any]

      Serialize item to a JSON-friendly dictionary.



.. py:class:: LinkCheck

   Verification result for a single customization entry inside a target root.


   .. py:attribute:: target_label
      :type:  str


   .. py:attribute:: kind
      :type:  CustomizationKind


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: repo
      :type:  str


   .. py:attribute:: link_path
      :type:  pathlib.Path


   .. py:attribute:: source_path
      :type:  pathlib.Path | None


   .. py:attribute:: status
      :type:  LinkStatus


   .. py:attribute:: detail
      :type:  str


   .. py:method:: to_dict() -> dict[str, Any]

      Serialize check to a JSON-friendly dictionary.



.. py:class:: StatusReport

   Aggregate report returned by `check_status`.


   .. py:attribute:: projects_dir
      :type:  pathlib.Path


   .. py:attribute:: scope
      :type:  ScopeName


   .. py:attribute:: canonical_items
      :type:  list[CustomizationItem]
      :value: []



   .. py:attribute:: checks
      :type:  list[LinkCheck]
      :value: []



   .. py:attribute:: collisions
      :type:  list[str]
      :value: []



   .. py:property:: managed_checks
      :type: list[LinkCheck]


      Return checks corresponding to canonical managed items.


   .. py:property:: unmanaged_checks
      :type: list[LinkCheck]


      Return checks corresponding to unmanaged stray entries.


   .. py:property:: all_ok
      :type: bool


      Return True if all canonical sources exist and all managed links are `ok`.


   .. py:method:: to_dict() -> dict[str, Any]

      Serialize full report to a JSON-friendly dictionary.



.. py:class:: SyncAction

   Result of synchronizing a single customization link.


   .. py:attribute:: target_label
      :type:  str


   .. py:attribute:: kind
      :type:  CustomizationKind


   .. py:attribute:: name
      :type:  str


   .. py:attribute:: link_path
      :type:  pathlib.Path


   .. py:attribute:: source_path
      :type:  pathlib.Path | None


   .. py:attribute:: action
      :type:  str


   .. py:attribute:: detail
      :type:  str


   .. py:method:: to_dict() -> dict[str, Any]

      Serialize sync action to a JSON-friendly dictionary.



.. py:class:: SyncReport

   Aggregate report returned by `sync_links`.


   .. py:attribute:: dry_run
      :type:  bool


   .. py:attribute:: scope
      :type:  ScopeName


   .. py:attribute:: actions
      :type:  list[SyncAction]
      :value: []



   .. py:attribute:: errors
      :type:  list[str]
      :value: []



   .. py:property:: ok
      :type: bool


      Return True if no errors occurred during synchronization.


   .. py:method:: to_dict() -> dict[str, Any]

      Serialize sync report to a JSON-friendly dictionary.



.. py:class:: TargetRoot

   A destination customization root (`.agents/` in a workspace or `~/.gemini/config`).


   .. py:attribute:: label
      :type:  str


   .. py:attribute:: scope
      :type:  Literal['workspaces', 'global']


   .. py:attribute:: root_path
      :type:  pathlib.Path


   .. py:method:: link_dir(kind: CustomizationKind) -> pathlib.Path

      Return the `skills/` or `agents/` subdirectory inside this target root.



.. py:class:: ToolRepoSpec

   Specification for a repository hosting canonical skills and subagent definitions.


   .. py:attribute:: rel_path
      :type:  str


   .. py:attribute:: expected_skills
      :type:  tuple[str, ...]
      :value: ()



   .. py:attribute:: expected_agents
      :type:  tuple[str, ...]
      :value: ()



   .. py:attribute:: excluded_skills
      :type:  frozenset[str]


   .. py:attribute:: excluded_agents
      :type:  frozenset[str]


.. py:function:: build_target_roots(projects_dir: pathlib.Path | None = None, global_config_dir: pathlib.Path | None = None, scope: ScopeName = 'all', workspace_names: collections.abc.Sequence[str] = DEFAULT_WORKSPACE_NAMES) -> list[TargetRoot]

   Build the ordered list of target customization roots for the requested scope.


.. py:function:: check_status(projects_dir: pathlib.Path | None = None, global_config_dir: pathlib.Path | None = None, scope: ScopeName = 'all', specs: collections.abc.Sequence[ToolRepoSpec] = DEFAULT_TOOL_REPO_SPECS, workspace_names: collections.abc.Sequence[str] = DEFAULT_WORKSPACE_NAMES) -> StatusReport

   Check canonical customization sources and symlink alignment across targets.


.. py:function:: discover_customizations(projects_dir: pathlib.Path | None = None, specs: collections.abc.Sequence[ToolRepoSpec] = DEFAULT_TOOL_REPO_SPECS) -> tuple[list[CustomizationItem], list[str]]

   Discover canonical skills and subagent definitions across configured tool repos.

   :param projects_dir: Base `PROJECTS` root containing `<org>/<repo>` folders.
   :param specs: Ordered sequence of tool repository specifications.

   :returns: A tuple `(items, collisions)` of deduplicated `CustomizationItem` records and
             collision warning messages.


.. py:function:: sync_links(projects_dir: pathlib.Path | None = None, global_config_dir: pathlib.Path | None = None, scope: ScopeName = 'all', dry_run: bool = False, replace_copies: bool = True, prune_unmanaged: bool = False, link_pending: bool = True, specs: collections.abc.Sequence[ToolRepoSpec] = DEFAULT_TOOL_REPO_SPECS, workspace_names: collections.abc.Sequence[str] = DEFAULT_WORKSPACE_NAMES) -> SyncReport

   Create or repair symlinks in workspace `.agents/` and `~/.gemini/config/`.

   :param projects_dir: Base `PROJECTS` root directory.
   :param global_config_dir: Global Antigravity config directory (`~/.gemini/config`).
   :param scope: Which targets to synchronize (`"all"`, `"workspaces"`, or `"global"`).
   :param dry_run: If True, report planned mutations without modifying the filesystem.
   :param replace_copies: If True, replace stale file/directory copies with symlinks.
   :param prune_unmanaged: If True, remove unmanaged entries in target directories.
   :param link_pending: If True, create symlinks even when a declared canonical file is pending.
   :param specs: Tool repository specifications.
   :param workspace_names: Workspace folder names under `projects_dir`.

   :returns: A `SyncReport` summarizing all actions and any filesystem errors.


