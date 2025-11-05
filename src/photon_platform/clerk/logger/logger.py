"""
PHOTON logger
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import Header, Footer, Static, Button, Input, Label

from rich import inspect, print
from rich.text import Text

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

LOG_TEMPLATE = "log.rst.j2"


class Logger(App):
    CSS_PATH = "logger.css"
    TITLE = "PHOTON • logger"
    BINDINGS = [
        ("ctrl+s", "save", "save"),
        ("ctrl+p", "screenshot", "screenshot"),
        ("ctrl+q", "quit", "quit"),
    ]

    def compose(self) -> ComposeResult:
        log_time = datetime.now()
        log_str = log_time.strftime("%y.%j-%H%M%S")
        yield Header()
        yield Footer()
        yield VerticalScroll(
            Label("LOG:"),
            Input(value=log_str, id="log"),
            Label("TITLE:"),
            Input(placeholder="title for log entry", id="title"),
            Label("EXCERPT:"),
            Input(placeholder="short desc", id="excerpt"),
            Label("TAGS:"),
            Input(placeholder="comma separated list", id="tags"),
            Label("CATEGORY:"),
            Input(placeholder="comma separated list", id="category"),
            Label("IMAGE:"),
            Input(placeholder="image path", id="image"),
            id="dialog",
            classes="form",
        )
        yield Button("Save", id="save")
        yield Button("Quit", id="quit")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "save":
            self.action_save()

        elif event.button.id == "quit":
            self.exit()

    def action_save(self):
        log_stamp = self.query_one("#log").value
        title = self.query_one("#title").value
        excerpt = self.query_one("#excerpt").value
        tags = self.query_one("#tags").value
        category = self.query_one("#category").value
        image = self.query_one("#image").value
        context = {
            "log_stamp": log_stamp,
            "title": title,
            "excerpt": excerpt,
            "tags": tags,
            "category": category,
            "image": image,
        }

        env = Environment(
            #  loader=FileSystemLoader(TEMPLATE_PATH),
            loader=PackageLoader("photon_platform.logger"),
        )
        template = env.get_template(LOG_TEMPLATE)
        rst_text = template.render(**context)

        file_path = Path(f"log/{log_stamp}")
        file_path.mkdir(parents=True, exist_ok=True)

        filename = file_path / "index.rst"
        filename.write_text(rst_text)

        self.exit(str(filename))

    def action_screenshot(self, path: str = "./") -> None:
        """Save an SVG "screenshot". This action will save an SVG file containing the current contents of the screen.

        Args:
        filename (str | None, optional): Filename of screenshot, or None to auto-generate. Defaults to None.
        path (str, optional): Path to directory. Defaults to "./".
        """
        self.bell()

        log_stamp = self.query_one("#log").value
        filename = f"log/{log_stamp}.svg"
        path = self.save_screenshot(filename, path)

        message = Text.assemble("Screenshot saved to ", (f"'{path}'", "bold green"))
        print(message)
        #  self.add_note(message)
        #  self.screen.mount(Notification(message))
