"""Clerk track core logic."""
import os
import re
from pathlib import Path
from typing import List, Dict, Optional

def get_frontmatter_and_content(file_path: Path) -> tuple[dict, str]:
    """Extract frontmatter and content from a markdown file.

    Assumes frontmatter is between the first two '---' lines.
    """
    try:
        text = file_path.read_text()
    except Exception as e:
        return {}, ""

    if text.startswith("---"):
        try:
            parts = text.split("---", 2)
            if len(parts) >= 3:
                frontmatter_str = parts[1]
                content = parts[2].strip()
                
                # Simple YAML parsing (only supporting 'order' for now)
                frontmatter = {}
                for line in frontmatter_str.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()
                return frontmatter, content
        except Exception:
            pass
            
    return {}, text

def get_todos(base_path: Path) -> Dict[str, List[Dict]]:
    """Scan for docsrc/todos/*.md files recursively from base_path.

    Returns a dictionary of relative paths to valid todo dictionaries.
    """
    todos_map = {}
    
    # Walk the directory tree
    for root, dirs, files in os.walk(base_path):
        root_path = Path(root)
        
        # Check if we are in a 'docsrc/todos' directory
        # OR if we are in a 'todos' directory (org level)
        # We look for files ending in .md
        
        is_todo_dir = False
        if root_path.name == "todos":
            # Check parent to see context
            if root_path.parent.name == "docsrc":
                 is_todo_dir = True
            elif "PROJECTS" in str(root_path): # simplistic check for org level todos
                 is_todo_dir = True
                 
        if is_todo_dir:
            for file in files:
                if file.endswith(".md"):
                    file_path = root_path / file
                    frontmatter, content = get_frontmatter_and_content(file_path)
                    
                    # We treat the file as a todo item
                    if frontmatter.get('order') or content: # Basic validation
                        order = frontmatter.get('order', '999')
                        try:
                            order = int(order)
                        except:
                            order = 999
                            
                        # Determine project name relative to base_path
                        # If base_path is /home/phi/PROJECTS
                        # file might be /home/phi/PROJECTS/geometor/elements/docsrc/todos/foo.md
                        # relative path: geometor/elements/docsrc/todos/foo.md
                        # Project: geometor/elements
                        
                        rel_path = file_path.relative_to(base_path)
                        project_parts = list(rel_path.parts)
                        
                        project_name = "Root"
                        if "docsrc" in project_parts:
                             idx = project_parts.index("docsrc")
                             project_name = "/".join(project_parts[:idx])
                        elif "todos" in project_parts:
                             idx = project_parts.index("todos")
                             # if todos is at root, empty list
                             if idx == 0:
                                 project_name = "Root"
                             else:
                                 project_name = "/".join(project_parts[:idx])

                        item = {
                            "file_path": str(file_path),
                            "filename": file,
                            "order": order,
                            "content": content,
                            "frontmatter": frontmatter
                        }
                        
                        if project_name not in todos_map:
                            todos_map[project_name] = []
                        todos_map[project_name].append(item)
                        
    return todos_map


import json
from rich.console import Console
from rich.padding import Padding

def report_todos_md(todos_map: Dict[str, List[Dict]]) -> None:
    """Print a formatted markdown report of todos."""
    print(f"# Clerk Track Report\n")
    
    # Sort projects alphabetically
    for project in sorted(todos_map.keys()):
        items = todos_map[project]
        if not items:
            continue
            
        print(f"## {project}")
        
        # Sort items by order
        sorted_items = sorted(items, key=lambda x: x['order'])
        
        for item in sorted_items:
            summary = _get_summary(item)
            print(f"- [ ] {summary} <!-- order: {item['order']} --> ([{item['filename']}]({item['file_path']}))")
        
        print("") # Newline between projects


def report_todos_rich(todos_map: Dict[str, List[Dict]], group_by_project: bool = False) -> None:
    """Print a formatted rich text report of todos."""
    console = Console()
    
    if group_by_project:
        # Existing Logic: Grouped by Project
        for project in sorted(todos_map.keys()):
            items = todos_map[project]
            if not items:
                continue
                
            console.print(f"[bold cyan]{project}[/bold cyan]")
            
            sorted_items = sorted(items, key=lambda x: x['order'])
            
            for item in sorted_items:
                _print_rich_item(console, item, show_project=False)

    else:
        # New Logic: Flat List (Ungrouped)
        all_items = []
        for project, items in todos_map.items():
            for item in items:
                item['project'] = project
                all_items.append(item)
                
        # Sort by order, then project, then filename
        sorted_items = sorted(all_items, key=lambda x: (x['order'], x['project'], x['filename']))
        
        for item in sorted_items:
            _print_rich_item(console, item, show_project=True)

def _print_rich_item(console: Console, item: Dict, show_project: bool = False) -> None:
    """Print a single todo item."""
    summary = _get_summary(item)
    order = item['order']
    filepath = item['file_path']
    project = item.get('project', '')
    
    order_str = f"{order:>3}"
    
    content_lines = item['content'].split('\n')
    rest_lines = []
    
    found_title = False
    for line in content_lines:
        clean_line = line.strip()
        if not found_title and clean_line.startswith('#') and summary in clean_line:
            found_title = True
            continue 
        
        if not rest_lines and not clean_line:
            continue
            
        rest_lines.append(line)

    header = f"[bold]{order_str}[/bold]"
    if show_project:
        header += f" [cyan]{project}[/cyan] -"
    
    header += f" [bold]{summary}[/bold]"
    
    console.print(header)
    
    if rest_lines:
        full_text = "\n".join(rest_lines)
        console.print(Padding(full_text, (0, 0, 0, 6)))
    
    console.print(f"      [dim]({filepath})[/dim]")
    console.print()


def report_todos_json(todos_map: Dict[str, List[Dict]]) -> None:
    """Print a JSON representation of todos."""
    # Enrich items with summary for JSON output too
    output_map = {}
    for project, items in todos_map.items():
        output_map[project] = []
        for item in items:
            item_copy = item.copy()
            item_copy['summary'] = _get_summary(item)
            output_map[project].append(item_copy)
            
    print(json.dumps(output_map, indent=2))

def report_todos_list(todos_map: Dict[str, List[Dict]]) -> None:
    """Print a simple list of todo titles, sorted globally by order."""
    all_items = []
    for project, items in todos_map.items():
        for item in items:
            item['project'] = project # Ensure project name is available
            all_items.append(item)
            
    # Sort by order, then project, then filename
    sorted_items = sorted(all_items, key=lambda x: (x['order'], x['project'], x['filename']))
    
    for item in sorted_items:
        summary = _get_summary(item)
        order_str = f"{item['order']:>3}"
        print(f"{order_str} {item['project']} - {summary}")

def _get_summary(item: Dict) -> str:
    """Extract title/summary from item content.

    Prioritizes the first Markdown heading (starting with #).
    Falls back to the first non-empty line.
    Falls back to filename.
    """
    content_lines = item['content'].split('\n')
    
    # First pass: look for header
    for line in content_lines:
        clean_line = line.strip()
        if clean_line.startswith('#'):
            return clean_line.lstrip('#').strip()
            
    # Second pass: first non-empty line
    for line in content_lines:
        clean_line = line.strip()
        if clean_line:
            return clean_line
            
    return item['filename']


