import ast
import sys
import os
from pathlib import Path

def get_stdlib_modules():
    with os.popen(f"{sys.executable} -c 'import sys; print(sys.path)'") as file:
        sys_path = eval(file.read().strip())
    stdlib_modules = set()
    for path in sys_path:
        if path.endswith('lib'):
            lib_path = Path(path)
            for module in lib_path.glob('**/*.py'):
                stdlib_modules.add(module.stem)
    return stdlib_modules

def get_imports_from_file(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()

    tree = ast.parse(source_code)
    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                imports.add(node.module.split('.')[0])

    return imports

def find_non_stdlib_imports(file_path):
    stdlib_modules = get_stdlib_modules()
    imports = get_imports_from_file(file_path)
    non_stdlib_imports = imports - stdlib_modules

    return non_stdlib_imports

if __name__ == "__main__":
    file_path = "path/to/your/python_file.py"
    non_stdlib_imports = find_non_stdlib_imports(file_path)
    print("Non-standard library imports:")
    for imp in non_stdlib_imports:
        print(imp)