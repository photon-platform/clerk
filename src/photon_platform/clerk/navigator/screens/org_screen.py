"""
Screen for organization-level navigation.
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Static
from textual.containers import Container
from pathlib import Path
import subprocess
from datetime import datetime
from photon_platform.clerk.navigator.widgets.dashboard import DashboardPanel

class OrgScreen(Screen):
    """Lists repositories within an organization."""
    
    BINDINGS = [
        ("j", "move_down", "Down"),
        ("k", "move_up", "Up"),
        ("l", "select_repo", "Select"),
        ("enter", "select_repo", "Select"),
        ("h", "navigate_back", "Back"),
    ]

    def __init__(self, org_path: Path):
        super().__init__()
        self.org_path = org_path
        self.repos = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(str(self.org_path), id="path-display")
        with Container(id="miller-columns"):
            yield DataTable(id="parent-table", classes="column")
            yield DataTable(id="org-table", classes="column")
            yield DashboardPanel(id="dashboard-panel")
        yield Footer()

    async def on_mount(self) -> None:
        p_table = self.query_one("#parent-table", DataTable)
        o_table = self.query_one("#org-table", DataTable)
        
        for t in [p_table, o_table]:
            t.add_column("Name")
            t.cursor_type = "row"
            
        await self.refresh_view()
        o_table.focus()
        
        # Determine context on mount
        if hasattr(self.app, "update_context"):
            self.app.update_context(self.org_path)

    def on_screen_resume(self) -> None:
        # Update context when we return to this screen
        if hasattr(self.app, "update_context"):
            self.app.update_context(self.org_path)

    async def refresh_view(self) -> None:
        """Refresh the view when view_mode or show_hidden changes."""
        view_mode = getattr(self.app, "view_mode", "dashboard")
        if view_mode == "dashboard":
            self.app.add_class("dashboard-view")
            self.app.remove_class("file-view")
            panel = self.query_one("#dashboard-panel", DashboardPanel)
            panel.update_org_stats(self.org_path)
        else:
            self.app.add_class("file-view")
            self.app.remove_class("dashboard-view")
            
        await self.load_repos()
        self.load_parent_column()
        
        # Focus management
        if getattr(self.app, "view_mode", "file") == "dashboard":
            self.query_one("#parent-table").focus()
        else:
            self.query_one("#org-table").focus()

    async def load_repos(self):
        o_table = self.query_one("#org-table", DataTable)
        o_table.clear()
        
        show_hidden = getattr(self.app, "show_hidden", False)
        
        repos = [d for d in self.org_path.iterdir() if d.is_dir()]
        if not show_hidden:
            repos = [r for r in repos if not r.name.startswith('.')]
            
        self.repos = sorted(repos)
        
        for repo in self.repos:
            icon = " "
            o_table.add_row(f"{icon}{repo.name}")

    def load_parent_column(self):
        p_table = self.query_one("#parent-table", DataTable)
        p_table.clear()
        parent = self.org_path.parent
        
        show_hidden = getattr(self.app, "show_hidden", False)
        
        try:
            items = [d for d in parent.iterdir() if d.is_dir()]
            if not show_hidden:
                items = [d for d in items if not d.name.startswith('.')]
            self.parent_items = sorted(items)
        except Exception:
            self.parent_items = []
        
        for i, item in enumerate(self.parent_items):
            icon = " "
            label = f"{icon}{item.name}"
            if item == self.org_path:
                p_table.add_row(f"> {label}")
                try:
                    p_table.move_cursor(row=i)
                except:
                    pass
            else:
                p_table.add_row(f"  {label}")

    async def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.data_table.id == "org-table":
            if event.cursor_row < len(self.repos):
                panel = self.query_one("#dashboard-panel", DashboardPanel)
                panel.update_repo_stats(self.repos[event.cursor_row])
        elif event.data_table.id == "parent-table":
             # If we are highlighting an org sibling, update org stats? 
             # Or just show org stats for the current org.
             pass

    async def action_move_up(self) -> None:
        table = self.focused
        if isinstance(table, DataTable) and table.cursor_row > 0:
            table.move_cursor(row=table.cursor_row - 1)

    async def action_move_down(self) -> None:
        table = self.focused
        if isinstance(table, DataTable) and table.cursor_row < table.row_count - 1:
            table.move_cursor(row=table.cursor_row + 1)

    async def action_select_repo(self) -> None:
        table = self.focused
        if not isinstance(table, DataTable):
            return
            
        row_index = table.cursor_row
        if row_index is not None:
            if table.id == "org-table":
                repo_path = self.repos[row_index]
            else: # parent-table
                repo_path = self.parent_items[row_index]
                
            from .repo_screen import RepoScreen
            self.app.push_screen(RepoScreen(repo_path))

    async def action_navigate_back(self) -> None:
        # Go back to PROJECTS level or home
        if len(self.app.screen_stack) > 2:
             self.app.pop_screen()
        else:
             # Universal navigation: Go up to parent folder in a RepoScreen
             parent = self.org_path.parent
             if parent != self.org_path:
                 from .repo_screen import RepoScreen
                 self.app.switch_screen(RepoScreen(parent))
             else:
                 self.app.action_quit()
