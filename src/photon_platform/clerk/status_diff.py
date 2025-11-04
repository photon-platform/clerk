#!/usr/bin/env python
import subprocess
import sys

def run_command(command):
    """Runs a shell command and returns its output."""
    try:
        result = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)
        return result.strip()
    except subprocess.CalledProcessError as e:
        print(f"""Error running command: {' '.join(e.cmd)}
{e.output}""")
        sys.exit(1)

def status_diff():
    """
    Shows a report of the current git status and the diff since branching from main.
    """
    print("=" * 80)
    print("GIT STATUS")
    print("=" * 80)
    status_output = run_command(['git', 'status', '--short'])
    print(status_output if status_output else "No changes.")

    # Find the merge base between the current branch and main
    merge_base = run_command(['git', 'merge-base', 'main', 'HEAD'])
    if not merge_base:
        print("\nCould not determine the merge base with 'main'.")
        sys.exit(1)

    print("\n" + "=" * 80)
    print(f"DIFF SUMMARY (since branching from main at commit {merge_base[:7]})")
    print("=" * 80)
    diff_stat_output = run_command(['git', 'diff', '--stat', merge_base])
    print(diff_stat_output)

    print("\n" + "=" * 80)
    print(f"FULL DIFF (since branching from main at commit {merge_base[:7]})")
    print("=" * 80)
    diff_output = run_command(['git', 'diff', merge_base])
    print(diff_output)
    print("\n" + "=" * 80)


if __name__ == "__main__":
    status_diff()
