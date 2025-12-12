import inspect
import ast
import graphviz


def ast_to_dot(tree):
    graph = graphviz.Digraph()
    graph.attr(rankdir="TB")

    class DotASTVisitor(ast.NodeVisitor):
        def generic_visit(self, node):
            graph.node(repr(node), label=f"{type(node).__name__}")
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
dot_graph.render("ast_tree.png", format="png", view=True)
