from typing import Any

from pydantic import BaseModel, ConfigDict, PrivateAttr, ValidationInfo, field_validator
from pydantic_core import PydanticCustomError

from cli.conf.format import name_from_camel_case
from cli.conf.storage import BasicNameStorage
from cli.conf.types import ConditionResultMapping


class Component(BaseModel):
    """
    A Zentra model for all React components.
    """

    _c_name = PrivateAttr(default=None)
    model_config = ConfigDict(use_enum_values=True)

    @property
    def core_import_str(self) -> str:
        """Stores the core import statement for the component."""
        filename = name_from_camel_case(self.c_name)
        return f'import {{ {self.c_name}**extra_parts**}} from "../ui/{filename}"\n'.replace(
            "'", " "
        )

    @property
    def c_name(self) -> str:
        """Stores the classname for the JSX builder."""
        return self._c_name if self._c_name else self.__class__.__name__

    def attr_str(self) -> str | None:
        """Creates an attribute string based on conditional logic. Used for JSX conversion."""
        return None

    def content_str(self) -> str | None:
        """Creates a content string based on conditional logic. Used for JSX conversion."""
        return None

    def unique_logic_str(self) -> str | None:
        """Creates a JSX string containing the unique logic associated to the component added to the component before the `return`."""
        return None

    def below_content_str(self) -> str | None:
        """Creates a JSX string containing content below the component. Often used in substitute of `content_str()`."""
        return None

    def import_str(self, extra_parts: str = None) -> str:
        """Creates a JSX string containing the import statements required for the component. Adds them to the top of the JSX file with the others.

        By default, returns the `core_import_str` property with an optional parameter `extra_parts` as `None`. When updating `extra_parts`, structure your overloaded function as follows:

        ```python
        def import_str(self) -> str:
            extra_parts = "..."  # Populate string
            core = super().import_str(extra_parts)
            return JSXContainer.imports(core=core)
        ```
        """
        return self.core_import_str.replace(
            "**extra_parts**", extra_parts if extra_parts else " "
        )

    @classmethod
    def map_to_str(cls, map: ConditionResultMapping) -> str:
        """Creates a string based on a provided `(condition, result)` mapping. Usable inside `attr_str()` or `content_str()`. Used for JSX conversion."""
        attributes = [result for condition, result in map if condition]
        return " ".join(attributes)


class Page(BaseModel):
    """
    A Zentra model for a single webpage of React components.

    Parameters:
    - `name` (`str`) - the name of the page
    - `components` (`list[Component]`) - a list of page components
    """

    name: str
    components: list[Component]

    def get_schema(self, node: BaseModel = None) -> dict:
        """Returns a JSON tree of the `Page` components as nodes with a type (the component name) and its attributes (attrs)."""
        if node is None:
            node = self

        if isinstance(node, list):
            return [self.get_schema(item) for item in node]

        formatted_schema = {
            "type": node.__class__.__name__,
            "attrs": node.model_dump(),
        }

        valid_attrs = ["content", "components", "fields"]
        components_attr = next(
            (attr for attr in valid_attrs if hasattr(node, attr)), None
        )

        if components_attr is not None:
            children = getattr(node, components_attr)

            # Handle leaf nodes
            if not isinstance(children, list):
                children = [children]

            if children:
                formatted_schema["children"] = [
                    self.get_schema(child) for child in children
                ]

        return formatted_schema


class Icon(BaseModel):
    """A Zentra model for [Radix Ui Icons](https://www.radix-ui.com/icons)."""

    name: str


class Zentra(BaseModel):
    """An application class for registering the components to create."""

    pages: list[Page] = []
    components: list[Component] = []
    names: BasicNameStorage = BasicNameStorage()

    @field_validator("pages", "components", "names", mode="plain")
    def prevent_init_editing(
        cls, value: Any, info: ValidationInfo
    ) -> PydanticCustomError:
        raise PydanticCustomError(
            "init_disabled",
            f"custom initalisation disabled for '{info.field_name}'. Remove '{info.field_name}' argument",
            dict(field_name=info.field_name, wrong_value=value),
        )

    def __set_type(
        self, component: BaseModel, valid_types: tuple[BaseModel, ...]
    ) -> type:
        """Checks a components type and assigns it accordingly."""
        base_type = component.__class__.__base__
        return base_type if base_type in valid_types else type(component)

    def register(self, components: list[Page | Component]) -> None:
        """Register a list of Zentra models to generate."""
        type_mapping: dict[BaseModel, list] = {
            Page: self.pages,
            Component: self.components,
        }
        valid_types = tuple(type_mapping.keys())

        for component in components:
            if not isinstance(component, valid_types):
                raise ValueError(
                    f"Invalid component type: {type(component)}.\nMust be (or inherit from) a list of either: {valid_types}.\n\nValid examples:\n  zentra.register([Page(...), Page(...)])\n  zentra.register([Accordion(...), Button(...)])\n  zentra.register([Page(...), Accordion(...)])\n"
                )

            comp_type = self.__set_type(component, valid_types)
            type_mapping[comp_type].append(component)

        self.fill_storage(pages=self.pages)

    def fill_storage(self, pages: list[Page]) -> None:
        """Populates page and component names into name storage."""
        filter_list = ["FormField"]
        component_names = self.__extract_component_names(pages)
        component_names = list(set(component_names) - set(filter_list))
        component_names.sort()

        self.names.components = component_names
        self.names.pages = [page.name for page in pages]
        self.names.filenames = [
            f"{name_from_camel_case(name)}.tsx" for name in self.names.components
        ]

    @staticmethod
    def __extract_component_names(pages: list[Page]) -> list[str]:
        """A helper function for retrieving the page component names."""
        component_names = set()

        def recursive_extract(component):
            if isinstance(component, list):
                for item in component:
                    recursive_extract(item)
            else:
                component_names.add(component.__class__.__name__)

            for attr in ["content", "fields"]:
                if hasattr(component, attr):
                    next_node = getattr(component, attr)
                    recursive_extract(next_node)

        for page in pages:
            for component in page.components:
                recursive_extract(component)

        component_names = list(component_names)
        component_names.sort()
        return component_names
