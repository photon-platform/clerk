"""The main application class for the viewer."""

import subprocess
from pathlib import Path
import os

from photon_platform.logger import Logger


def find_git_home_directory():
    """
    Find the Git home directory starting from the current directory.
    Returns the path to the Git home directory as a Path object if found, otherwise returns None.
    """
    try:
        # Run the git command to get the top-level directory
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        # Handle cases where the current directory is not part of a Git repository
        print("Error: Current directory is not part of a Git repository.")
        return None


def get_docsrc_directory():
    """
    Check if a 'docsrc' directory exists in the Git home directory.
    If it exists, returns the full path to 'docsrc', otherwise returns None.
    Additionally, sets the current working directory to 'docsrc' if it exists.
    """
    git_home = find_git_home_directory()
    if git_home:
        docsrc_path = git_home / 'docsrc'
        if docsrc_path.exists():
            # Set the current working directory to the 'docsrc' directory
            os.chdir(docsrc_path)
            return docsrc_path
        else:
            print("'docsrc' directory does not exist in the Git home directory.")
            return None
    return None


def run() -> None:
    """Run the application."""
    docsrc_directory = get_docsrc_directory()
    if docsrc_directory:
        print(f"Current directory is now set to 'docsrc': {docsrc_directory}")
    else:
        print("Failed to set current directory to 'docsrc'.")
    reply = Logger().run()
    print(reply)

    if reply:
        subprocess.run(["vim", reply])

if __name__ == "__main__":
    run()
