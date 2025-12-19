"""
Screen for file preview and agent actions.
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.containers import Vertical, ScrollableContainer
from rich.syntax import Syntax
from pathlib import Path

class FileScreen(Screen):
    """Provides a preview of a file and actions for coordination."""
    
    BINDINGS = [
        ("h", "app.pop_screen", "Back"),
        ("j", "scroll_down", "Down"),
        ("k", "scroll_up", "Up"),
        ("e", "edit_file", "Edit"),
        ("A", "export_for_agent", "Agent Export"),
    ]

    def __init__(self, file_path: Path):
        super().__init__()
        self.file_path = file_path

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield Static(f"File: {self.file_path.name}", id="file-header")
            with ScrollableContainer(id="preview-container"):
                yield Static(id="preview-content")
        yield Footer()

    def on_mount(self) -> None:
        self.update_preview()

    def action_scroll_up(self) -> None:
        self.query_one("#preview-container").scroll_up()

    def action_scroll_down(self) -> None:
        self.query_one("#preview-container").scroll_down()

    def update_preview(self) -> None:
        try:
            content = self.file_path.read_text()
            lexer = Syntax.guess_lexer(str(self.file_path))
            syntax = Syntax(content, lexer, theme="monokai", line_numbers=True)
            self.query_one("#preview-content").update(syntax)
        except Exception as e:
            self.query_one("#preview-content").update(f"Error loading preview: {e}")

    def action_edit_file(self) -> None:
        # Placeholder for launching vim
        self.notify(f"Launching vim for {self.file_path.name}")
        import subprocess
        self.app.suspend_reporting()
        subprocess.run(["vim", str(self.file_path)])
        self.app.resume_reporting()
        self.update_preview()

    def action_export_for_agent(self) -> None:
        context = self.app.clerk_context
        export_text = context.export_for_agent()
        export_text += f"\nFILE: {self.file_path.name}\n"
        
        export_path = Path("/home/phi/PROJECTS/photon-platform/agent_context.txt")
        export_path.write_text(export_text)
        
        self.notify(f"Context exported to {export_path.name}")
