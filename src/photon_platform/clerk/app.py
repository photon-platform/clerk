"""
run the main app
"""
from .clerk import Clerk


def run() -> None:
    reply = Clerk().run()
    print(reply)
