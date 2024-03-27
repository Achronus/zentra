from cli.conf.format import name_from_camel_case
from zentra.core import Component


class ComponentJSXBuilder:
    """A builder for creating the JSX representation of the components."""

    def __init__(self, component: Component) -> None:
        self.component = component

        self.attr_str = ""
        self.content_str = ""

        self.import_statement = ""
        self.component_str = ""
        self.unique_logic_str = ""

        self.classname = self.component.__class__.__name__

        self.no_content = False
        self.no_unique_logic = False

        self.build()

    def __repr__(self) -> str:
        """Create a readable developer string representation of the object when using the `print()` function."""
        attributes = ", ".join(
            f"{key}={value!r}" for key, value in self.__dict__.items()
        )
        return f"{self.classname}({attributes})"

    def build(self) -> None:
        """Builds the component string based on the component values."""
        self.set_import()
        self.set_attrs()
        self.set_content()
        self.set_unique_logic()

        self.set_component_str()

    def set_import(self) -> None:
        """Sets the component import statement."""
        filename = name_from_camel_case(self.classname)
        self.import_statement = (
            f'import { {self.classname} } from "../ui/{filename}"'.replace("'", " ")
        )

    def set_component_str(self) -> None:
        """Combines the outer shell of the component with its attributes and content."""
        if self.no_content:
            self.component_str = f"<{self.classname}{self.attr_str}/>"
        else:
            self.component_str = f"<{self.classname}{self.attr_str}>{self.content_str}</{self.classname}>"

    def set_attrs(self) -> None:
        """Populates the `attr_str` based on the component values."""
        self.attr_str = " " + self.component.attr_str()

    def set_content(self) -> None:
        """Populates the `content_str` based on the component values."""
        try:
            self.content_str = self.component.content_str()
        except NotImplementedError:
            self.no_content = True

    def set_unique_logic(self) -> None:
        """Populates the `unique_logic_str` based on the component values."""
        try:
            self.unique_logic_str = self.component.unique_logic_str()
        except NotImplementedError:
            self.no_unique_logic = True
