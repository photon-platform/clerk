import inspect
import ast
import graphviz


def ast_to_dot(tree):
    graph = graphviz.Digraph()
    graph.attr(rankdir="TB")

    class DotASTVisitor(ast.NodeVisitor):
        def generic_visit(self, node):
            label = None

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                label = f"def {node.name}"
            elif isinstance(node, ast.ClassDef):
                label = f"class {node.name}"
            elif isinstance(node, ast.Import):
                names = ", ".join(alias.name for alias in node.names)
                label = f"import {names}"
            elif isinstance(node, ast.ImportFrom):
                names = ", ".join(alias.name for alias in node.names)
                label = f"from {node.module} import {names}"
            elif isinstance(node, ast.Call):
                func_name = ast.unparse(node.func).strip()
                label = f"call {func_name}"

            if label is not None:
                graph.node(repr(node), label=label)
                if hasattr(node, "parent"):
                    graph.edge(repr(node.parent), repr(node))

            for child in ast.iter_child_nodes(node):
                child.parent = node
                self.visit(child)

    DotASTVisitor().visit(tree)
    return graph


import requests as testmodule

source_code = inspect.getsource(testmodule)

tree = ast.parse(source_code)
dot_graph = ast_to_dot(tree)
print(dot_graph)
dot_graph.render("simplified_ast_tree.png", format="png", view=True)
