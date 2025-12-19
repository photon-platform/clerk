"""
Clerk Navigator Application.
"""
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Container
from pathlib import Path

from ..context import Context, determine_context
from .screens.org_screen import OrgScreen
from .screens.repo_screen import RepoScreen

class ClerkNavigator(App):
    """A context-sensitive navigation TUI for the PHOTON platform."""
    
    CSS_PATH = "navigator.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        (".", "toggle_hidden", "Hidden Files"),
        ("F", "set_file_view", "File View"),
        ("D", "set_dashboard_view", "Dashboard"),
    ]

    def __init__(self, context: Context):
        super().__init__()
        self.clerk_context = context
        self.show_hidden = False
        self.view_mode = "dashboard"
        self.exit_path = None

    def update_context(self, new_path: Path):
        """Update the global context with the new navigation path."""
        self.clerk_context.path = new_path.resolve()
        # Optionally update other context fields if needed, or re-run determine_context
        # simple update for now
        self.exit_path = self.clerk_context.path

    async def action_set_file_view(self) -> None:
        self.view_mode = "file"
        self._manual_view_override = True
        self.remove_class("dashboard-view")
        self.add_class("file-view")
        self.notify("Switched to File View")
        if hasattr(self.screen, "refresh_view"):
            await self.screen.refresh_view()
            # In File view, focus the current table
            try:
                self.screen.query_one("#current-table").focus()
            except Exception:
                pass

    async def action_set_dashboard_view(self) -> None:
        self.view_mode = "dashboard"
        self._manual_view_override = True
        self.remove_class("file-view")
        self.add_class("dashboard-view")
        self.notify("Switched to Dashboard")
        if hasattr(self.screen, "refresh_view"):
            await self.screen.refresh_view()
            # In Dashboard view, focus the parent table
            try:
                self.screen.query_one("#parent-table").focus()
            except Exception:
                pass

    def compose(self) -> ComposeResult:
        # Initial class
        self.add_class(f"{self.view_mode}-view")
        yield Header()
        yield Container(id="main-container")
        yield Footer()

    def on_mount(self) -> None:
        if self.clerk_context.repo_name and self.clerk_context.project_root:
            self.push_screen(RepoScreen(self.clerk_context.project_root))
        elif self.clerk_context.org_name:
            # Assuming org_path is PROJECTS/org_name
            org_path = Path("/home/phi/PROJECTS") / self.clerk_context.org_name
            self.push_screen(OrgScreen(org_path))
        else:
            # Fallback to projects listing or current dir
            self.notify("Unknown context, showing current directory.")
            self.push_screen(RepoScreen(self.clerk_context.path))

    def action_toggle_hidden(self) -> None:
        self.show_hidden = not self.show_hidden
        self.notify(f"{'Showing' if self.show_hidden else 'Hiding'} hidden files")
        if hasattr(self.screen, "refresh_view"):
            # If the screen's refresh_view is async, it should be called accordingly.
            # However, textual actions are often sync and can call async methods.
            import asyncio
            if asyncio.iscoroutinefunction(self.screen.refresh_view):
                asyncio.create_task(self.screen.refresh_view())
            else:
                self.screen.refresh_view()

    def action_quit(self) -> None:
        self.exit(self.exit_path)
