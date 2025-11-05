"""
run the main app
"""
from .projector import Projector


def run() -> None:
    reply = Projector().run()
    print(reply)
