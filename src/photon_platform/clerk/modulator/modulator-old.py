from pathlib import Path
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader("photon_platform.modulator", "templates"))

def create_module(project_path: Path, namespace_name: str, module_name: str) -> None:
    namespace_name = namespace_name.replace(" ", "_").replace("-", "_")
    namespace_dir = (
        project_path / "src" / namespace_name
    )
    module_name = module_name.replace(" ", "_").replace("-", "_")
    module_dir = namespace_dir / module_name
    module_dir.mkdir(parents=True, exist_ok=True)

    context = {
            "namespace_name": namespace_name,
            "module_name": module_name,
            "author": "PHOTON platform",
            }
    init_template = env.get_template("__init__.py.j2")
    with (module_dir / "__init__.py").open("w") as f:
        f.write(init_template.render(**context))

    main_template = env.get_template("__main__.py.j2")
    with (module_dir / "__main__.py").open("w") as f:
        f.write(main_template.render(**context))

    app_template = env.get_template("app.py.j2")
    with (module_dir / "app.py").open("w") as f:
        f.write(app_template.render(**context))

    with (module_dir / f"{module_name}.py").open("w") as f:
        f.write(f'"""\n{module_name}\n"""')


def create_class(
    project_path: Path, namespace_name: str, module_name: str, class_name: str
) -> None:
    namespace_dir = (
        project_path / "src" / namespace_name.replace(" ", "_").replace("-", "_")
    )
    module_dir = namespace_dir / module_name.replace(" ", "_").replace("-", "_")
    class_file = module_dir / f"{class_name}.py"

    class_template = env.get_template("{class_name}.py")
    with class_file.open("w") as f:
        f.write(f'"""\n{class_name}\n"""')


def create_submodule(
    project_path: Path, namespace_name: str, module_name: str, submodule_name: str
) -> None:
    namespace_dir = (
        project_path / "src" / namespace_name.replace(" ", "_").replace("-", "_")
    )
    module_dir = namespace_dir / module_name.replace(" ", "_").replace("-", "_")
    submodule_dir = module_dir / submodule_name.replace(" ", "_").replace("-", "_")
    submodule_dir.mkdir(parents=True, exist_ok=True)

    init_template = env.get_template("__init__.py")
    with (submodule_dir / "__init__.py").open("w") as f:
        f.write(init_template.render(module_name=submodule_name, author="phiarchitect"))

    submodule_template = env.get_template("{module_name}.py")
    with (submodule_dir / f"{submodule_name}.py").open("w") as f:
        f.write(submodule_template.render(module_name=submodule_name))


def create_module_function(
    project_path: Path, 
    namespace_name: str,
    module_name: str,
    function_name: str,
    args: str,
    return_type: str,
) -> None:
    namespace_dir = (
        project_path / "src" / namespace_name.replace(" ", "_").replace("-", "_")
    )
    module_dir = namespace_dir / module_name.replace(" ", "_").replace("-", "_")
    function_file = module_dir / f"{module_name}.py"

    function_template = env.get_template("function.py")
    with function_file.open("a") as f:
        f.write(
            function_template.render(
                function_name=function_name, args=args, return_type=return_type
            )
        )


def create_class_method(
    project_path: Path,
    namespace_name: str,
    module_name: str,
    class_name: str,
    method_name: str,
    args: str,
    return_type: str,
) -> None:
    namespace_dir = (
        project_path / "src" / namespace_name.replace(" ", "_").replace("-", "_")
    )
    module_dir = namespace_dir / module_name.replace(" ", "_").replace("-", "_")
    class_file = module_dir / f"{class_name}.py"

    method_template = env.get_template("method.py")
    with class_file.open("a") as f:
        f.write(
            method_template.render(
                method_name=method_name, args=args, return_type=return_type
            )
        )
