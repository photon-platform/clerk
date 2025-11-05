"""
PHOTON lister
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Button, Input

from rich import inspect, print
from rich.text import Text

from datetime import datetime
from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape

LOG_TEMPLATE = 'log.rst.j2'


class Lister(App):
    CSS_PATH = "logger.css"
    TITLE = "PHOTON • log lister"
    BINDINGS = [
            ('ctrl+s', 'save', 'save'),
            ('ctrl+p', 'screenshot', 'screenshot'),
            ('ctrl+q', 'quit', 'quit'),
            ]

    def compose(self) -> ComposeResult:
        log_time = datetime.now()
        log_str = log_time.strftime('%y.%j-%H%M%S')
        yield Header()
        yield Footer()
        yield Container(
            Static('LOG:', classes='label'),
            Input(value=log_str, id='log'),
            Static('TITLE:', classes='label'),
            Input(placeholder='Note Title', id='title'),
            Static('EXCERPT:', classes='label'),
            Input(placeholder='short desc', id='excerpt'),
            Static('TAGS:', classes='label'),
            Input(placeholder='comma separated list', id='tags'),
            Static('CATEGORY:', classes='label'),
            Input(placeholder='comma separated list', id='category'),
            Static(),
            Button("Save", id='save'),
            Static(),
            Button("Quit", id='quit'),
            id="dialog",
            classes="form"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        if event.button.id == "save":
            self.action_save()

        elif event.button.id == "quit":
            self.exit()

    def action_save(self):
        log_stamp = self.query_one('#log').value
        title = self.query_one('#title').value
        excerpt = self.query_one('#excerpt').value
        tags = self.query_one('#tags').value
        category = self.query_one('#category').value
        context = {
                'log_stamp': log_stamp,
                'title': title,
                'excerpt': excerpt,
                'tags': tags,
                'category': category
                }

        env = Environment(
            #  loader=FileSystemLoader(TEMPLATE_PATH),
            loader=PackageLoader('photonplatform.logger'),
            )
        template = env.get_template(LOG_TEMPLATE)
        rst_text = template.render(**context)

        filename = f'log/{log_stamp}.rst'
        file_path = Path(filename)
        file_path.write_text(rst_text)

        self.exit(filename)

    def action_screenshot(self, path: str = "./") -> None:
        """Save an SVG "screenshot". This action will save an SVG file containing the current contents of the screen.

        Args:
            filename (str | None, optional): Filename of screenshot, or None to auto-generate. Defaults to None.
            path (str, optional): Path to directory. Defaults to "./".
        """
        self.bell()

        log_stamp = self.query_one('#log').value
        filename = f'log/{log_stamp}.svg'
        path = self.save_screenshot(filename, path)

        message = Text.assemble("Screenshot saved to ", (f"'{path}'", "bold green"))
        print(message)
        #  self.add_note(message)
        #  self.screen.mount(Notification(message))


if __name__ == "__main__":
    import subprocess

    app = Lister()
    reply = app.run()
    print(reply)

    if reply:
        subprocess.run(['vim', reply])

