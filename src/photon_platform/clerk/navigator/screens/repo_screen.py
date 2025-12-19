from pathlib import Path
import subprocess
from datetime import datetime
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, DataTable, Static, Label
from textual.containers import Vertical, Horizontal, Container
from rich.syntax import Syntax
from photon_platform.clerk.navigator.widgets.dashboard import DashboardPanel
from photon_platform.clerk.navigator.screens.file_screen import FileScreen

class RepoScreen(Screen):
    """Lists files and directories within a repository with Miller columns."""
    
    BINDINGS = [
        ("j", "move_down", "Down"),
        ("k", "move_up", "Up"),
        ("l", "select_item", "Open"),
        ("enter", "select_item", "Open"),
        ("h", "navigate_back", "Back"),
        ("s", "jump_to_source", "Source"),
        ("d", "jump_to_docs", "Docs"),
        ("t", "jump_to_tests", "Tests"),
    ]

    def __init__(self, repo_path: Path):
        super().__init__()
        self.repo_path = repo_path
        self.current_path = repo_path
        self.current_items = []
        self.parent_items = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(str(self.current_path), id="path-display")
        # Miller columns container
        with Container(id="miller-columns"):
            # Parent directory table
            yield DataTable(id="parent-table", classes="column")
            # Current directory table
            yield DataTable(id="current-table", classes="column")
            # Dashboard Panel (replaces middle/right in dashboard mode)
            yield DashboardPanel(id="dashboard-panel")
            # Preview pane (Static or another DataTable)
            yield Static(id="preview-pane", classes="column")
        yield Footer()

    async def on_mount(self) -> None:
        p_table = self.query_one("#parent-table", DataTable)
        c_table = self.query_one("#current-table", DataTable)
        
        for t in [p_table, c_table]:
            t.add_column("Name")
            t.cursor_type = "row"
            
        await self.refresh_view()
        # In dashboard mode, focus parent table. In file mode, focus current table.
        if getattr(self.app, "view_mode", "file") == "dashboard":
            p_table.focus()
        else:
            c_table.focus()

    async def refresh_view(self) -> None:
        """Refresh the current view based on current state."""
        # Update app classes if we changed view mode
        view_mode = getattr(self.app, "view_mode", "file")
        if view_mode == "dashboard":
            self.app.add_class("dashboard-view")
            self.app.remove_class("file-view")
        else:
            self.app.add_class("file-view")
            self.app.remove_class("dashboard-view")
            
        await self.load_directory(self.current_path)

    async def load_directory(self, path: Path):
        c_table = self.query_one("#current-table", DataTable)
        c_table.clear()
        self.current_path = path
        self.query_one("#path-display").update(str(self.current_path))
        
        # Update global app context for shell integration
        if hasattr(self.app, "update_context"):
            self.app.update_context(path)

        # Check for "special" folders to determine default view mode
        is_special = (
            path == self.repo_path or 
            any(part in ["src", "docsrc", "docs", "tests"] for part in path.parts)
        )
        
        if not hasattr(self.app, "_manual_view_override"):
            self.app.view_mode = "dashboard" if is_special else "file"
            
        if getattr(self.app, "view_mode", "file") == "dashboard":
            panel = self.query_one("#dashboard-panel", DashboardPanel)
            # Use the current path to find the relevant project root for stats
            panel.update_repo_stats(path)

        view_mode = getattr(self.app, "view_mode", "dashboard")
        show_hidden = getattr(self.app, "show_hidden", False)
        
        # List directories first, then files
        dirs = [d for d in path.iterdir() if d.is_dir()]
        files = [f for f in path.iterdir() if f.is_file()]
        
        if not show_hidden:
            dirs = [d for d in dirs if not d.name.startswith('.')]
            files = [f for f in files if not f.name.startswith('.')]
            
        self.current_items = sorted(dirs) + sorted(files)

        for item in self.current_items:
            icon = " " if item.is_dir() else " "
            c_table.add_row(f"{icon}{item.name}")

        self.load_parent_column()
        if self.current_items:
            self.update_preview(self.current_items[0])

    def load_parent_column(self):
        p_table = self.query_one("#parent-table", DataTable)
        p_table.clear()
        parent = self.current_path.parent
        
        show_hidden = getattr(self.app, "show_hidden", False)
        
        # We only show siblings if the current path is within the repo or we are at repo root
        # If we are at repo root, parent siblings might be other repos
        items = [d for d in parent.iterdir() if d.is_dir()]
        if not show_hidden:
            items = [d for d in items if not d.name.startswith('.')]
            
        self.parent_items = sorted(items)
        
        for i, item in enumerate(self.parent_items):
            icon = " "
            label = f"{icon}{item.name}"
            # Highlight the current directory in the parent list
            if item == self.current_path:
                p_table.add_row(f"> {label}")
                try:
                    p_table.move_cursor(row=i)
                except Exception:
                    pass
            else:
                p_table.add_row(f"  {label}")

    def update_preview(self, item: Path):
        preview = self.query_one("#preview-pane") # Changed from #preview-content
        view_mode = getattr(self.app, "view_mode", "dashboard")

        if item.is_dir():
            try:
                sub_items = sorted([f.name for f in item.iterdir() if not f.name.startswith('.')][:20])
                preview.update("\n".join([f" {n}" for n in sub_items]))
            except Exception:
                preview.update("Error reading directory")
        elif view_mode == "dashboard" and item.suffix == ".py":
             # Symbols view for Python
             try:
                 import ast
                 content = item.read_text()
                 tree = ast.parse(content)
                 symbols = []
                 for node in ast.walk(tree):
                     if isinstance(node, ast.ClassDef):
                         symbols.append(f"󰌗 {node.name}")
                     elif isinstance(node, ast.FunctionDef):
                         symbols.append(f"󰊕 {node.name}")
                 preview.update("\n".join(symbols) or "No symbols found")
             except Exception as e:
                 preview.update(f"Error parsing symbols: {e}")
        elif view_mode == "dashboard" and item.suffix in [".rst", ".md"]:
            # Title list for docs
            try:
                import re
                content = item.read_text()
                titles = re.findall(r"^(?:#|==+)\s*(.*)", content, re.MULTILINE)
                preview.update("\n".join([f"󰈙 {t}" for t in titles]) or "No titles found")
            except Exception:
                preview.update("Error parsing titles")
        else:
            try:
                content = item.read_text()[:1000] # preview first 1k chars
                lexer = Syntax.guess_lexer(str(item))
                syntax = Syntax(content, lexer, theme="monokai")
                preview.update(syntax)
            except Exception:
                preview.update("Binary file or error reading")

    async def on_data_table_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.data_table.id == "current-table":
            if event.cursor_row < len(self.current_items):
                self.update_preview(self.current_items[event.cursor_row])
        elif event.data_table.id == "parent-table":
            # In dashboard mode, we want the panel to show stats for the sibling project we are highlighting
            if getattr(self.app, "view_mode", "file") == "dashboard":
                if event.cursor_row < len(self.parent_items):
                    panel = self.query_one("#dashboard-panel", DashboardPanel)
                    panel.update_repo_stats(self.parent_items[event.cursor_row])

    async def action_move_up(self) -> None:
        table = self.focused
        if not isinstance(table, DataTable):
             # Fallback to intelligent default based on view mode
             if getattr(self.app, "view_mode", "file") == "dashboard":
                  table = self.query_one("#parent-table", DataTable)
             else:
                  table = self.query_one("#current-table", DataTable)
             table.focus()
             
        if table.cursor_row > 0:
            table.move_cursor(row=table.cursor_row - 1)

    async def action_move_down(self) -> None:
        table = self.focused
        if not isinstance(table, DataTable):
             if getattr(self.app, "view_mode", "file") == "dashboard":
                  table = self.query_one("#parent-table", DataTable)
             else:
                  table = self.query_one("#current-table", DataTable)
             table.focus()

        if table.cursor_row < table.row_count - 1:
            table.move_cursor(row=table.cursor_row + 1)

    async def action_parent_prev(self) -> None:
        p_table = self.query_one("#parent-table", DataTable)
        if p_table.cursor_row > 0:
            new_idx = p_table.cursor_row - 1
            new_path = self.parent_items[new_idx]
            await self.load_directory(new_path)

    async def action_parent_next(self) -> None:
        p_table = self.query_one("#parent-table", DataTable)
        if p_table.cursor_row < p_table.row_count - 1:
            new_idx = p_table.cursor_row + 1
            new_path = self.parent_items[new_idx]
            await self.load_directory(new_path)

    async def action_select_item(self) -> None:
        # Select from the FOCUSED table
        table = self.focused
        if not isinstance(table, DataTable):
             if getattr(self.app, "view_mode", "file") == "dashboard":
                  table = self.query_one("#parent-table", DataTable)
             else:
                  table = self.query_one("#current-table", DataTable)
             table.focus()
            
        row_index = table.cursor_row
        if row_index is not None:
            if table.id == "current-table":
                selected_item = self.current_items[row_index]
            else: # parent-table
                selected_item = self.parent_items[row_index]
                
            if selected_item.is_dir():
                await self.load_directory(selected_item)
            else:
                from photon_platform.clerk.navigator.screens.file_screen import FileScreen
                self.app.push_screen(FileScreen(selected_item))

    async def action_navigate_back(self) -> None:
        if self.current_path != self.repo_path:
            await self.load_directory(self.current_path.parent)
        else:
            # We are at the root of the repo (or whatever folder we started in).
            # If we have a screen history, pop.
            if len(self.app.screen_stack) > 1:
                self.app.pop_screen()
            elif self.app.clerk_context.org_name:
                # If we are in a known context stack, maybe go to org?
                # But universal navigation says we should just go up.
                # Let's check if parent is manageable.
                parent = self.current_path.parent
                # If we are essentially at root, maybe quit?
                if parent == self.current_path:
                     self.app.action_quit()
                else:
                     # Go to parent directory in a new RepoScreen (universal browse)
                     # Or technically we can just re-use this screen if we change self.repo_path?
                     # Creating a new screen is cleaner for history.
                     # However, to simulate "up", we might want to SWITCH to OrgScreen if parent is an Org?
                     # The prompt implies "Universal Exploration".
                     # If we just switch_screen to a RepoScreen of parent:
                     await self.app.switch_screen(RepoScreen(parent))
            else:
                 # Fallback
                 parent = self.current_path.parent
                 if parent != self.current_path:
                      await self.app.switch_screen(RepoScreen(parent))
                 else:
                      self.app.action_quit()

    async def action_jump_to_source(self) -> None:
        # Try to find src folder
        target = self.repo_path / "src"
        if target.exists() and target.is_dir():
            # Try to find first __init__.py package
            found = False
            for child in target.iterdir():
                if child.is_dir() and (child / "__init__.py").exists():
                    target = child
                    found = True
                    break
            
            await self.load_directory(target)
            await self.app.action_set_file_view()
        else:
            self.app.notify("No src directory found")

    async def action_jump_to_docs(self) -> None:
        target = self.repo_path / "docsrc"
        if not target.exists():
            target = self.repo_path / "docs"
        
        if target.exists() and target.is_dir():
            await self.load_directory(target)
            await self.app.action_set_dashboard_view()
        else:
            self.app.notify("No docs directory found")
            
    async def action_jump_to_tests(self) -> None:
        target = self.repo_path / "tests"
        
        if target.exists() and target.is_dir():
            await self.load_directory(target)
            await self.app.action_set_file_view()
        else:
            self.app.notify("No tests directory found")
