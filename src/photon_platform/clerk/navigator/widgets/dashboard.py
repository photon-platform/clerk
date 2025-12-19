from textual.app import ComposeResult
from textual.widgets import Static
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from pathlib import Path
from typing import Optional
import subprocess
import os

class DashboardPanel(Static):
    """A panel for situational awareness showing project or org stats."""
    
    def update_repo_stats(self, path: Path):
        """Update the panel with repository-specific statistics."""
        project_root = self.find_project_root(path)
        stats = self.gather_repo_stats(project_root or path)
        
        table = Table.grid(expand=True)
        table.add_column(style="bold cyan", width=20)
        table.add_column(style="yellow")

        table.add_row("Project:", (project_root or path).name)
        table.add_row("Version:", stats.get("version", "N/A"))
        table.add_row("Git Branch:", stats.get("branch", "N/A"))
        table.add_row("Git Status:", stats.get("git_status", "Clean"))
        table.add_row("", "") # Spacer
        
        table.add_row("Source Files:", str(stats.get("src_files", 0)))
        table.add_row("Lines of Code:", str(stats.get("src_loc", 0)))
        table.add_row("Doc Files:", str(stats.get("doc_files", 0)))
        table.add_row("", "") # Spacer
        
        # Intelligent Previews
        table.add_row("[bold magenta]Intelligent Preview:[/bold magenta]", "")
        previews = stats.get("previews", [])
        if previews:
            for p in previews[:8]:
                table.add_row("", p)
        else:
            table.add_row("", "[italic]No previews available[/italic]")
        
        self.update(Panel(
            table, 
            title="[bold magenta]Project Dashboard[/bold magenta]", 
            border_style="magenta",
            padding=(1, 2)
        ))

    def find_project_root(self, path: Path) -> Optional[Path]:
        """Climb up from path to find a .git or pyproject.toml."""
        current = path.resolve()
        while current != current.parent:
            if (current / ".git").exists() or (current / "pyproject.toml").exists():
                return current
            current = current.parent
        return None

    def update_org_stats(self, org_path: Path):
        """Update the panel with organization-level awareness."""
        repos = [d for d in org_path.iterdir() if d.is_dir() and (d / ".git").exists()]
        
        content = Text.assemble(
            ("Organization: ", "bold cyan"), (org_path.name, "yellow"), "\n",
            ("Total Repos: ", "bold cyan"), (str(len(repos)), "yellow"), "\n",
            ("\nSituational Awareness:\n", "bold magenta"),
            ("All systems operational.", "green")
        )
        self.update(Panel(content, title="Org Dashboard", border_style="magenta"))

    def gather_repo_stats(self, repo_path: Path) -> dict:
        stats = {}
        try:
            # Git info
            stats["branch"] = subprocess.check_output(
                ["git", "branch", "--show-current"], 
                cwd=repo_path, stderr=subprocess.DEVNULL
            ).decode().strip()
            dirty = subprocess.check_output(
                ["git", "status", "--short"], 
                cwd=repo_path
            ).decode().strip()
            stats["git_status"] = "Dirty" if dirty else "Clean"
            
            # Version
            pyproject_path = repo_path / "pyproject.toml"
            version = "N/A"
            if pyproject_path.exists():
                import tomllib
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    version = data.get("project", {}).get("version")
                    if not version and "version" in data.get("project", {}).get("dynamic", []):
                        attr = data.get("tool", {}).get("setuptools", {}).get("dynamic", {}).get("version", {}).get("attr")
                        if attr:
                            # Guess path from attribute (e.g. photon_platform.clerk.__version__)
                            parts = attr.split(".")
                            path_parts = ["src"] + parts[:-1] + ["__init__.py"]
                            ver_file = repo_path.joinpath(*path_parts)
                            if ver_file.exists():
                                import re
                                match = re.search(r'__version__\s*=\s*["\'](.*?)["\']', ver_file.read_text())
                                if match: version = match.group(1)
            stats["version"] = version or "N/A"
            
            # Source stats
            src_path = repo_path / "src"
            if src_path.exists():
                src_files = list(src_path.rglob("*.py"))
                stats["src_files"] = len(src_files)
                loc = 0
                for f in src_files:
                    try:
                        with open(f, "r", errors="ignore") as fp:
                            loc += sum(1 for line in fp if line.strip())
                    except: pass
                stats["src_loc"] = loc
            
            # Doc stats
            doc_path = repo_path / "docsrc"
            if not doc_path.exists(): doc_path = repo_path / "docs"
            if doc_path.exists():
                doc_files = list(doc_path.rglob("*.rst")) + list(doc_path.rglob("*.md"))
                stats["doc_files"] = len(doc_files)

            # Intelligent Previews (Symbols/Titles)
            previews = []
            # Try finding a meaningful file to preview
            search_patterns = ["README.rst", "README.md", "src/**/__init__.py", "src/**/app.py"]
            for pattern in search_patterns:
                if "**" in pattern:
                     matches = list(repo_path.rglob(pattern.split("**/")[-1]))
                else:
                     matches = list(repo_path.glob(pattern))
                
                if matches:
                    f = matches[0]
                    if f.suffix == ".py":
                        try:
                            import ast
                            tree = ast.parse(f.read_text())
                            for node in ast.walk(tree):
                                if isinstance(node, ast.ClassDef): previews.append(f"󰌗 {node.name}")
                                elif isinstance(node, ast.FunctionDef): previews.append(f"󰊕 {node.name}")
                                if len(previews) >= 8: break
                        except: pass
                    elif f.suffix in [".rst", ".md"]:
                        try:
                            import re
                            titles = re.findall(r"^(?:#|==+)\s*(.*)", f.read_text(), re.MULTILINE)
                            previews = [f"󰈙 {t}" for t in titles[:8]]
                        except: pass
                    if previews: break
            stats["previews"] = previews
                
        except Exception as e:
            stats["error"] = str(e)
            
        return stats
