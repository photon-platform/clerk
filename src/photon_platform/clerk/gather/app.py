"""
run the main app
"""
from .gather import Gather


def run() -> None:
    reply = Gather().run()
    print(reply)
