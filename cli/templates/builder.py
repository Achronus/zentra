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

        self.build()

    def __repr__(self) -> str:
        """Create a readable developer string representation of the object when using the `print()` function."""
        class_name = self.__class__.__name__
        attributes = ", ".join(
            f"{key}={value!r}" for key, value in self.__dict__.items()
        )
        return f"{class_name}({attributes})"

    def build(self) -> None:
        """Builds the component string based on the component values."""
        self.set_name()
        self.set_import()
        self.set_attrs()
        self.set_content()

        self.component_str = self.component_str.replace("**attrs**", self.attr_str)
        self.component_str = self.component_str.replace("**content**", self.content_str)

    def set_import(self) -> None:
        """Sets the component import statement."""
        classname = self.component.__class__.__name__
        filename = name_from_camel_case(classname)
        self.import_statement = (
            f'import { {classname} } from "../ui/{filename}"'.replace("'", " ")
        )

    def set_name(self) -> None:
        """Creates the outer shell of the component."""
        name = self.component.__class__.__name__
        self.component_str = f"<{name}**attrs**>**content**</{name}>"

    def set_attrs(self) -> None:
        """Populates the `attr_str` based on the component values."""
        self.attr_str = self.component.attr_str()

    def set_content(self) -> None:
        """Populates the `content_str` based on the component values."""
        self.content_str = self.component.content_str()
