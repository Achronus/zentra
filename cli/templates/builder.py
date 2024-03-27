from cli.conf.format import name_from_camel_case
from zentra.core import Component


class ComponentJSXBuilder:
    """A builder for creating the JSX representation of the components."""

    def __init__(self, component: Component) -> None:
        self.component = component

        self.attr_str = None
        self.content_str = None
        self.unique_logic_str = None
        self.below_content_str = None

        self.import_statement = ""
        self.component_str = ""

        self.classname = self.component.__class__.__name__

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
        self.set_below_content()

        self.set_component_str()

    def set_import(self) -> None:
        """Sets the component import statement."""
        filename = name_from_camel_case(self.classname)
        self.import_statement = (
            f'import { {self.classname} } from "../ui/{filename}"'.replace("'", " ")
        )

    def set_component_str(self) -> None:
        """Combines the outer shell of the component with its attributes and content."""
        if self.content_str:
            self.component_str = f"<{self.classname}{self.attr_str}>{self.content_str}</{self.classname}>"
        else:
            self.component_str = f"<{self.classname}{self.attr_str} />"

        if self.below_content_str:
            self.component_str += self.below_content_str

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
