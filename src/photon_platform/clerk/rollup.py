
import os
import subprocess
from datetime import datetime
import toml
import glob
import re


def get_version_file():
    for filename in glob.iglob('src/**/__init__.py', recursive=True):
        with open(filename, 'r') as f:
            if re.search(r'^__version__\s*=\s*".*"', f.read(), re.M):
                return filename
    return None


def get_version():
    version_file = get_version_file()
    if not version_file:
        return None
    with open(version_file, 'r') as f:
        content = f.read()
    match = re.search(r'^__version__\s*=\s*"(.*)"', content, re.M)
    if match:
        return match.group(1)
    return None


def update_version(new_version):
    version_file = get_version_file()
    if not version_file:
        return
    with open(version_file, "r") as f:
        content = f.read()
    new_content = re.sub(r'__version__\s*=\s*".*"', f'__version__ = "{new_version}"', content)
    with open(version_file, "w") as f:
        f.write(new_content)

def update_changelog(new_version):
    changelog_path = "CHANGELOG.rst"
    with open(changelog_path, "r") as f:
        content = f.read()
    
    new_entry = f"""{new_version}
-----
*{datetime.now().strftime("%Y-%m-%d")}*

**fixed**

.. + 

**added**

.. + 

**changed**

.. + 
"""
    
    with open(changelog_path, "w") as f:
        f.write(f"changelog\n=========\n\n{new_entry}\n{content}")

def rollup():
    # 1. Get current branch
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip().decode('utf-8')

    # 2. Get version
    version = get_version()
    print(f"Current version: {version}")

    # 3. Increment patch version
    major, minor, patch = version.split('.')
    new_version = f"{major}.{minor}.{int(patch) + 1}"
    print(f"New version: {new_version}")

    # 4. Update version in __init__.py
    update_version(new_version)

    # 5. Update CHANGELOG.md
    update_changelog(new_version)

    # 6. Stage and commit all changes
    subprocess.run(['git', 'add', '.'])
    commit_message = f"ROLLUP: Version {new_version}"
    subprocess.run(['git', 'commit', '-m', commit_message])

    # 7. Merge to main
    subprocess.run(['git', 'switch', 'main'])
    subprocess.run(['git', 'merge', current_branch])
    subprocess.run(['git', 'push'])

    # 8. Tag and push tag
    subprocess.run(['git', 'tag', f'v{new_version}'])
    subprocess.run(['git', 'push', '--tags'])

    # 9. Delete feature branch
    subprocess.run(['git', 'branch', '-d', current_branch])

if __name__ == '__main__':
    rollup()
