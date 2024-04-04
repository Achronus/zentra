from typing import Callable
from cli.conf.format import name_from_camel_case

from pydantic import BaseModel

from zentra.core import Component, Page
from zentra.ui import Form


# (attribute_name, lambda_expression)
AttributeMapping = list[tuple[str, Callable]]

# (component_type, attribute_name, lambda_expression)
ComponentAttributesMapping = list[tuple[Component, str, Callable]]


# Dictionary of components with containers around them
# (classname, attributes)
COMPONENTS_TO_WRAP = {
    "Checkbox": 'className="flex items-top space-x-2"',
}

# Components that have a "use client" import at the top of their file
USE_CLIENT_COMPONENTS = [
    "Calendar",
    "Checkbox",
    "Collapsible",
]


class JSXMappings(BaseModel):
    """A storage container for JSX mappings."""

    common_attrs: AttributeMapping
    component_attrs: list[tuple]


class JSXPageContentStorage(BaseModel):
    """
    A storage container for the pieces of a JSX Zentra `Page` model.

    Parameters:
    - `imports` (`list[string]`) - a list of strings representing import statements
    - `props` (`list[string]`) - a list of strings representing the TypeScript props
    - `logic` (`list[string]`) - a list of strings representing the component function logic
    - `content` (`list[string]`) - a list of strings containing the JSX content used in the return statement
    - `form_schema` (`list[string], optional`) - a list of strings representing the form schema, if the page contains a form. `None` by default
    """

    imports: list[str] = []
    props: list[str] = []
    logic: list[str] = []
    content: list[str] = []
    form_schema: list[str] = None


class JSXComponentContentStorage(BaseModel):
    """
    A storage container for the pieces of a JSX Zentra `Component` model.

    Parameters:
    - `imports` (`list[string]`) - a list of strings representing import statements
    - `props` (`list[string]`) - a list of strings representing the TypeScript props
    - `logic` (`list[string]`) - a list of strings representing the component function logic
    - `attributes` (`list[string]`) - a list of strings representing the attributes used in the main component
    - `jsx` (`list[string]`) - a list of strings containing the JSX content used in the return statement
    """

    imports: list[str] = []
    props: list[str] = []
    logic: list[str] = []
    attributes: list[str] = []
    jsx: list[str] = []


class JSXPageBuilder:
    """A builder for creating Zentra `Page` models as JSX."""

    def __init__(self, page: Page, mappings: JSXMappings) -> None:
        self.page = page
        self.mappings = mappings

        self.storage = JSXPageContentStorage()
        self.jsx = ""

    def build(self) -> str:
        """Builds the JSX for the page."""
        for component in self.page.components:
            builder = ComponentBuilder(component=component, mappings=self.mappings)
            builder.build(container=self.storage)

        return self.concat_content()

    def concat_content(self) -> str:
        """Compresses the storage values into a single string of JSX content."""
        imports = self.dedupe_n_compress(self.storage.imports)
        props = self.compress(self.storage.props)
        logic = self.compress(self.storage.logic)
        content = self.compress(self.storage.content)

        return "".join(imports + props + logic + content)

    def compress(self, values: list[str]) -> str:
        """Compresses an attributes values into a string."""
        return "\n".join(values)

    def dedupe(self, values: list[str]) -> list[str]:
        """Filters out duplicate values from the list."""
        return list(set(values))

    def dedupe_n_compress(self, values: list[str]) -> str:
        """Filters out duplicate values from a list and compresses them into a single string."""
        return self.compress(self.dedupe(values))


class FormBuilder:
    """A builder for creating Zentra `Form` models as JSX."""

    def __init__(self, form: Form) -> None:
        self.form = form

    def build(self) -> str:
        """Builds the JSX for the form."""
        for field in self.form:
            # TODO: access sub-components
            # field.content
            pass


class AttributeBuilder:
    """A builder for creating Zentra `Component` attributes."""

    def __init__(self, mappings: JSXMappings) -> None:
        self.maps = mappings

    def build(self, component: Component) -> list[str]:
        """Builds the attributes from a mapping for the component."""
        attrs = []

        for attr_name, condition in self.maps.common_attrs:
            if hasattr(component, attr_name):
                value = getattr(component, attr_name)
                attr_str = condition(value)
                if attr_str:
                    attrs.append(attr_str)

        for item in self.maps.component_attrs:
            comp_type, attr_name, condition = item
            if isinstance(component, comp_type):
                value = getattr(component, attr_name)
                if value:
                    attrs += condition(value)
        return attrs


class ComponentBuilder:
    """A builder for creating Zentra `Component` models as JSX."""

    def __init__(self, component: Component, mappings: JSXMappings) -> None:
        self.component = component

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(mappings=mappings)

    def build(self, container: JSXPageContentStorage) -> None:
        """Builds the JSX for the component."""
        container.imports.append(self.core_import())
        self.storage.attributes = self.attrs.build(self.component)
        print(self.component.classname, self.storage.attributes)

    def core_import(self) -> str:
        """Creates the core import statement for the component."""
        filename = name_from_camel_case(self.component.classname)
        return f'import {{ {self.component.classname} }} from "../{self.component.library}/{filename}"'.replace(
            "'", " "
        )


class ComponentJSXBuilder:
    """A builder for creating the JSX representation of the components."""

    def __init__(self, component: Component) -> None:
        self.component = component

        self.attr_str = None
        self.content_str = None
        self.unique_logic_str = None
        self.below_content_str = None

        self.import_statements = ""
        self.component_str = ""

        self.classname = self.component.classname

        self.build()

    def __repr__(self) -> str:  # pragma: no cover
        """Create a readable developer string representation of the object when using the `print()` function."""
        attributes = ", ".join(
            f"{key}={value!r}" for key, value in self.__dict__.items()
        )
        return f"{self.classname}({attributes})"

    def build(self) -> None:
        """Builds the component string based on the component values."""
        self.set_attrs()
        self.set_content()
        self.set_unique_logic()
        self.set_below_content()

        self.set_imports()
        self.set_component_str()

    def set_imports(self) -> None:
        """Sets the component import statements."""
        if self.classname in USE_CLIENT_COMPONENTS:
            self.import_statements += '"use_client"\n\n'

        self.import_statements += self.component.import_str()

    def set_component_str(self) -> None:
        """Combines the outer shell of the component with its attributes and content."""
        if self.content_str:
            self.component_str = f"<{self.classname}{self.attr_str}>{self.content_str}</{self.classname}>"
        else:
            self.component_str = f"<{self.classname}{self.attr_str} />"

        if self.below_content_str:
            self.component_str += self.below_content_str

        if self.classname in COMPONENTS_TO_WRAP.keys():
            self.component_str = (
                f"<div {COMPONENTS_TO_WRAP[self.classname]}>{self.component_str}</div>"
            )

    def set_attrs(self) -> None:
        """Populates the `attr_str` based on the component values."""
        self.attr_str = " " + self.component.attr_str()

    def set_content(self) -> None:
        """Populates the `content_str` based on the component values."""
        self.content_str = self.component.content_str()

    def set_unique_logic(self) -> None:
        """Populates the `unique_logic_str` based on the component values."""
        self.unique_logic_str = self.component.unique_logic_str()

    def set_below_content(self) -> None:
        """Populates the `below_content_str` based on the component values."""
        self.below_content_str = self.component.below_content_str()
