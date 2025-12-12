import inspect
import parso
import graphviz

# test module
import requests as testmodule


def parso_to_dot(module):
    graph = graphviz.Digraph()
    graph.attr(rankdir="TB")

    def escape_label(label):
        return (
            label.replace("<", "\\<")
            .replace(">", "\\>")
            .replace('"', '\\"')
            .replace("{", "\\{")
            .replace("}", "\\}")
        )

    def visit(node):
        graph.node(repr(node), label=escape_label(f"{type(node).__name__}"))

        parent = node.parent
        if parent is not None:
            graph.edge(repr(parent), repr(node))

        if hasattr(node, "children"):
            for child_node in node.children:
                visit(child_node)

    visit(module)
    return graph


# Get the source code of the module
source_code = inspect.getsource(testmodule)

# Parse the source code using Parso
module = parso.parse(source_code)

# Process the module as needed
# For example, you can use the previously defined `parso_to_dot` function to visualize the module's structure
dot_graph = parso_to_dot(module)
dot_graph.render("requests_module.dot", view=True)
#  dot_graph.render("requests_module.png", format="png")

#  print(dot_graph)
