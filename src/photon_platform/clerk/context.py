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
    
    @property
    def is_project(self) -> bool:
        return self.project_root is not None

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
        
    # If we didn't find a project root but we are in an org folder (or deeper/shallower?)
    # If we are strictly in ~/PROJECTS/<org>, we might have set org_name above.
    
    if not context.org_name:
        # Fallback check if simple path parsing works
        # e.g. path is ~/PROJECTS/org/repo/subdir
        # find "PROJECTS" in parts
        try:
             parts = path.parts
             if "PROJECTS" in parts:
                 idx = parts.index("PROJECTS")
                 if idx + 1 < len(parts):
                     context.org_name = parts[idx+1]
                 if idx + 2 < len(parts):
                     # If we didn't establish this is a project root via markers, 
                     # we might still want to guess repo name? 
                     # But safer to rely on markers for repo identity to avoid bare folders.
                     pass 
        except ValueError:
            pass

    return context
