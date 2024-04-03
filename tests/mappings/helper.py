from cli.templates.jsx import ComponentJSXBuilder
from zentra.core import Component


def builder(component: Component) -> ComponentJSXBuilder:
    return ComponentJSXBuilder(component)
