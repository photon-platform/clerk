"""
PHOTON logger
"""
from rich import print
from rich.text import Text
from datetime import datetime
from pathlib import Path
from jinja2 import Environment, PackageLoader

LOG_TEMPLATE = "log.rst.j2"

def create_log_entry(project_root, title, excerpt, tags, category, image):
    """
    Creates a new log entry in docsrc/log.
    """
    log_time = datetime.now()
    log_stamp = log_time.strftime("%y.%j-%H%M%S")
    
    context = {
        "log_stamp": log_stamp,
        "title": title,
        "excerpt": excerpt,
        "tags": tags,
        "category": category,
        "image": image,
    }

    env = Environment(
        loader=PackageLoader("photon_platform.clerk.logger"),
    )
    template = env.get_template(LOG_TEMPLATE)
    rst_text = template.render(**context)

    # Path structure: <project_root>/docsrc/log/<log_stamp>/index.rst
    file_path = project_root / "docsrc" / "log" / log_stamp
    file_path.mkdir(parents=True, exist_ok=True)

    filename = file_path / "index.rst"
    filename.write_text(rst_text)
    
    return str(filename)
