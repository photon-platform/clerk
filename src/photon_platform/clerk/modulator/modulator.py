from pathlib import Path
from jinja2 import Environment, PackageLoader

class Modulator:
    def __init__(self, project_path: Path, namespace: str):
        self.project_path = project_path
        self.namespace = self._clean(namespace)
        self.env = Environment(loader=PackageLoader("photon_platform.modulator", "templates"))

    def create_module(self, module_name: str) -> None:
        module_name = self._clean(module_name)
        module_dir = self.project_path / "src" / self.namespace / module_name
        module_dir.mkdir(parents=True, exist_ok=True)

        context = {
            "namespace_name": self.namespace,
            "module_name": module_name,
            "author": "PHOTON platform",
        }
        self._render_template("__init__.py.j2", context, module_dir / "__init__.py")
        self._render_template("__main__.py.j2", context, module_dir / "__main__.py")
        self._render_template("app.py.j2", context, module_dir / "app.py")

        with (module_dir / f"{module_name}.py").open("w") as f:
            f.write(f'"""\n{module_name}\n"""')

    def create_submodule(self, module_name: str, submodule_name: str) -> None:
        self.create_module(f"{self._clean(module_name)}.{self._clean(submodule_name)}")

    def create_class(self, module_name: str, class_name: str) -> None:
        class_name = self._clean(class_name)
        module_dir = self.project_path / "src" / self.namespace / self._clean(module_name)
        class_file = module_dir / f"{class_name}.py"

        context = {
            "class_name": class_name
        }
        self._render_template("class.py.j2", context, class_file)

    def create_function(self, module_name: str, function_name: str, args: str, return_type: str) -> None:
        module_dir = self.project_path / "src" / self.namespace / self._clean(module_name)
        function_file = module_dir / f"{self._clean(module_name)}.py"

        context = {
            "function_name": self._clean(function_name),
            "args": self._clean(args),
            "return_type": return_type
        }
        self._render_template("function.py.j2", context, function_file, mode="a")

    def create_class_method(
        self, module_name: str, class_name: str, method_name: str, args: str, return_type: str
    ) -> None:
        module_dir = self.project_path / "src" / self.namespace / self._clean(module_name)
        class_file = module_dir / f"{self._clean(class_name)}.py"

        context = {
            "method_name": self._clean(method_name),
            "args": self._clean(args),
            "return_type": return_type
        }
        self._render_template("method.py.j2", context, class_file, mode="a")

    def _render_template(self, template_name: str, context: dict, output_path: Path, mode: str = "w") -> None:
        template = self.env.get_template(template_name)
        with output_path.open(mode) as f:
            f.write(template.render(**context))

    def _clean(self, name: str) -> str:
        return name.replace(" ", "_").replace("-", "_")

