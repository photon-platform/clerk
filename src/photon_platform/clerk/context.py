"""
Context detection for Clerk.
"""
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class Context:
    path: Path
    org_name: Optional[str] = None
    repo_name: Optional[str] = None
    project_root: Optional[Path] = None
    git_branch: Optional[str] = None
    is_dirty: bool = False
    
    @property
    def is_project(self) -> bool:
        return self.project_root is not None

    @property
    def is_src(self) -> bool:
        return self.path.match("**/src*") or "src" in self.path.parts

    @property
    def is_docs(self) -> bool:
        return any(self.path.match(f"**/{d}*") for d in ["docs", "docsrc"]) or any(d in self.path.parts for d in ["docs", "docsrc"])

    @property
    def is_tests(self) -> bool:
        return self.path.match("**/tests*") or "tests" in self.path.parts

    def export_for_agent(self) -> str:
        """Export the current context as a structured string for agents."""
        lines = [
            f"PATH: {self.path}",
            f"ORG: {self.org_name or 'N/A'}",
            f"REPO: {self.repo_name or 'N/A'}",
            f"BRANCH: {self.git_branch or 'N/A'}",
            f"DIRTY: {self.is_dirty}",
            f"TYPE: {'Project' if self.is_project else 'Generic'}",
        ]
        if self.is_src: lines.append("CONTEXT: Source Code")
        if self.is_docs: lines.append("CONTEXT: Documentation")
        if self.is_tests: lines.append("CONTEXT: Tests")
        
        return "\n".join(lines)

def determine_context(path: Path) -> Context:
    """
    Determine the context based on the current path.
    Assumes a structure of ~/PROJECTS/<org>/<repo> or git/pyproject markers.
    """
    path = path.resolve()
    context = Context(path=path)
    
    # Climb up to find project markers
    current = path
    while current != current.parent:
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            context.project_root = current
            context.repo_name = current.name
            
            # Git status info
            if (current / ".git").exists():
                try:
                    import subprocess
                    branch = subprocess.check_output(
                        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                        cwd=current, stderr=subprocess.DEVNULL
                    ).decode().strip()
                    context.git_branch = branch
                    
                    status = subprocess.check_output(
                        ["git", "status", "--porcelain"],
                        cwd=current, stderr=subprocess.DEVNULL
                    ).decode().strip()
                    context.is_dirty = bool(status)
                except Exception:
                    pass

            # Check for org (parent of repo)
            # Assuming ~/PROJECTS/<org>/<repo>
            projects_dir = current.parent.parent
            if projects_dir.name == "PROJECTS":
                context.org_name = current.parent.name
            break
        
        # Check if we are at the org level directly
        # Assuming path is ~/PROJECTS/<org>
        if current.parent.name == "PROJECTS":
             context.org_name = current.name
             break

        current = current.parent
        
    if not context.org_name:
        try:
             parts = path.parts
             if "PROJECTS" in parts:
                 idx = parts.index("PROJECTS")
                 if idx + 1 < len(parts):
                     context.org_name = parts[idx+1]
        except ValueError:
            pass

    return context
