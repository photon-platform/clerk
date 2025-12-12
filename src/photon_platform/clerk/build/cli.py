import click
from pathlib import Path
from .modulator import Modulator

def resolve_project_path(ctx, path):
    context = ctx.obj.get('context')
    if path:
        return Path(path)
    if context and context.is_project:
        return context.project_root
    return Path(click.prompt("Project Path"))

def resolve_namespace(ctx, namespace):
    context = ctx.obj.get('context')
    if namespace:
        return namespace
    if context and context.is_project and context.repo_name:
        return context.repo_name.replace('-', '_')
    return click.prompt("Namespace")

@click.group()
def build():
    """Shapes Python modules and packages."""
    pass

@build.command('module')
@click.option('--project-path', help='The path to the project.')
@click.option('--namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the module.')
@click.pass_context
def create_module(ctx, project_path, namespace, module_name):
    """Creates a new Python module."""
    path = resolve_project_path(ctx, project_path)
    ns = resolve_namespace(ctx, namespace)
    
    modulator = Modulator(path, ns)
    modulator.create_module(module_name)
    click.echo(f"Module {module_name} created successfully.")

@build.command('submodule')
@click.option('--project-path', help='The path to the project.')
@click.option('--namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the parent module.')
@click.option('--submodule-name', prompt='Submodule Name', help='The name of the submodule.')
@click.pass_context
def create_submodule(ctx, project_path, namespace, module_name, submodule_name):
    """Creates a new Python submodule."""
    path = resolve_project_path(ctx, project_path)
    ns = resolve_namespace(ctx, namespace)

    modulator = Modulator(path, ns)
    modulator.create_submodule(module_name, submodule_name)
    click.echo(f"Submodule {submodule_name} created successfully in {module_name}.")

@build.command('class')
@click.option('--project-path', help='The path to the project.')
@click.option('--namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the module.')
@click.option('--class-name', prompt='Class Name', help='The name of the class.')
@click.pass_context
def create_class(ctx, project_path, namespace, module_name, class_name):
    """Creates a new Python class."""
    path = resolve_project_path(ctx, project_path)
    ns = resolve_namespace(ctx, namespace)

    modulator = Modulator(path, ns)
    modulator.create_class(module_name, class_name)
    click.echo(f"Class {class_name} created successfully in {module_name}.")

@build.command('function')
@click.option('--project-path', help='The path to the project.')
@click.option('--namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the module.')
@click.option('--function-name', prompt='Function Name', help='The name of the function.')
@click.option('--args', prompt='Arguments', help='The arguments for the function.')
@click.option('--return-type', prompt='Return Type', help='The return type of the function.')
@click.pass_context
def create_function(ctx, project_path, namespace, module_name, function_name, args, return_type):
    """Creates a new Python function."""
    path = resolve_project_path(ctx, project_path)
    ns = resolve_namespace(ctx, namespace)

    modulator = Modulator(path, ns)
    modulator.create_function(module_name, function_name, args, return_type)
    click.echo(f"Function {function_name} created successfully in {module_name}.")

@build.command('method')
@click.option('--project-path', help='The path to the project.')
@click.option('--namespace', help='The namespace for the module.')
@click.option('--module-name', prompt='Module Name', help='The name of the module.')
@click.option('--class-name', prompt='Class Name', help='The name of the class.')
@click.option('--method-name', prompt='Method Name', help='The name of the method.')
@click.option('--args', prompt='Arguments', help='The arguments for the method.')
@click.option('--return-type', prompt='Return Type', help='The return type of the method.')
@click.pass_context
def create_class_method(ctx, project_path, namespace, module_name, class_name, method_name, args, return_type):
    """Creates a new Python class method."""
    path = resolve_project_path(ctx, project_path)
    ns = resolve_namespace(ctx, namespace)

    modulator = Modulator(path, ns)
    modulator.create_class_method(module_name, class_name, method_name, args, return_type)
    click.echo(f"Method {method_name} created successfully in class {class_name}.")
