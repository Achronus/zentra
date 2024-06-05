from typing import Union
from cli.conf.format import name_from_camel_case
from cli.conf.types import MappingDict

from cli.templates.builders.nodes import (
    ComponentNode,
    HTMLNode,
    IconNode,
    JSNode,
    StringNode,
)
from cli.templates.ui.mappings.storage import AttributeMappings
from cli.templates.utils import remove_none, text_content

from zentra.base import ZentraModel
from zentra.base.html import HTMLTag
from zentra.base.js import JSIterable
from zentra.core import Component
from zentra.core.react import LucideIcon
from zentra.core.utils import compress
from zentra.ui import Form


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
    """
    A builder for creating Zentra `Component` attributes.

    Parameters:
    - `component` (`zentra.core.Component`) - any Zentra Component model
    - `common_mapping` (`dictionary[string, callable]`) - a mapping containing common attributes across all components. With a `{key: value}` pair = `{attr_name, attr_func}`
    - `component_mapping` (`dictionary[string, callable]`) - a mapping containing unique component specific logic. With a `{key: value}` pair = `{component_name: attr_func}`.
    """

    def __init__(
        self,
        component: Component,
        common_mapping: MappingDict,
        component_mapping: MappingDict,
    ) -> None:
        self.component = component
        self.common_map = common_mapping
        self.component_map = component_mapping

    def get_common_attr(self, key: str, value: int | str | bool) -> str:
        """Retrieves an attribute string from the common attribute mapping given a key, value pair."""
        return self.common_map[key](value)

    def get_component_attrs(self) -> list[str]:
        """Retrieves a list of unique attribute strings for the component from the component attribute mapping."""
        return self.component_map[self.component.classname](self.component)

    def common_checks(self, attr_name: str) -> bool:
        """Performs checks for model attributes to confirm whether it should use the `common_map`. These include:
          1. When the `attr_name` is not an `inner_attribute`
          2. When the `attr_name` is not a `custom_common_attribute`

        If both checks are valid, returns `True`. Otherwise, returns `False`.
        """
        not_inner_attr = attr_name not in self.component.inner_attributes
        not_custom_attr = attr_name not in self.component.custom_common_attributes

        if not_inner_attr and not_custom_attr:
            return True

        return False

    def build(self) -> list[str]:
        """Builds the attributes from a mapping for the component."""
        attrs = []
        include_common = True
        model_dict = self.component.__dict__

        for attr_name, value in model_dict.items():
            if value is not None and attr_name in self.common_map.keys():
                include_common = self.common_checks(attr_name)

                if include_common:
                    attr_str = self.get_common_attr(attr_name, value)
                    attrs.append(attr_str)

        if (
            isinstance(self.component, Component)
            and self.component.classname in self.component_map.keys()
        ):
            attr_list = self.get_component_attrs()

            if attr_list is not None:
                attrs.extend(attr_list)

        return remove_none(attrs)


class ImportBuilder:
    """A builder for creating Zentra `Component` import statements."""

    def __init__(
        self, component: Component, additional_imports_mapping: MappingDict
    ) -> None:
        self.component = component
        self.additional_map = additional_imports_mapping

    def build(self) -> list[str]:
        """Builds the import statements for the component."""
        additional_imports = self.additional_imports()
        imports = []

        if not self.component.composition_only:
            imports.append(self.core_import())

        if additional_imports:
            imports.extend(additional_imports)

        return [item for item in imports if item]

    def core_import(self, child_names: list[str] = None) -> str:
        """Creates the core import statement for the component."""
        filename = name_from_camel_case(self.component.classname)
        import_pieces = self.core_import_pieces(
            child_names if child_names else self.component.child_names
        )
        return f'import {{ {import_pieces} }} from "@/components/{self.component.library}/{filename}"'.replace(
            "'", " "
        )

    def get_imports_from_map(self) -> list[str]:
        """A helper function to retrieve the additional imports from the `additional_map` for the component."""
        return self.additional_map[self.component.classname](self.component)

    def additional_imports(self) -> list[str]:
        """Creates the additional imports needed for the component."""
        imports = []

        if (
            isinstance(self.component, Component)
            and self.component.classname in self.additional_map.keys()
        ):
            import_list = self.get_imports_from_map()

            if import_list is not None:
                imports.extend(import_list)

        if len(imports) == 0:
            return None

        return imports

    def core_import_pieces(self, child_names: list[str]) -> str:
        """Creates the core import pieces including the main component and its children (if required)."""
        return ", ".join([self.component.classname] + child_names)


class ContentBuilder:
    """A builder for retrieving Zentra model content."""

    def __init__(
        self,
        model: ZentraModel,
        mapping: MappingDict,
    ) -> None:
        self.model = model
        self.model_map = mapping

    def get_content(self, model: ZentraModel) -> Union[ZentraModel, list[ZentraModel]]:
        """A helper function to retrieve the content from the `model_map` for the zentra model."""
        return self.model_map[model.classname](model)

    def build(self) -> list[ZentraModel | str]:
        """Builds the content for the model."""
        # Handle unique component models
        if self.model.classname in self.model_map.keys():
            return self.get_content(self.model)

        # Handle other models
        content = []
        if self.model.content_attributes:
            for attr_name in self.model.content_attributes:
                items = getattr(self.model, attr_name)

                if items:
                    if isinstance(items, list):
                        content.extend(items)
                    else:
                        content.append(items)

        return content


class LogicBuilder:
    """A builder for creating the Zentra `Component` function logic created above the `return` statement."""

    def __init__(self, component: Component, logic_mapping: MappingDict) -> None:
        self.component = component
        self.logic_map = logic_mapping

    def get_logic_list(self) -> list[str]:
        """A helper function to retrieve the logic statements from the `logic_map` for the component."""
        return self.logic_map[self.component.classname](self.component)

    def build(self) -> list[str]:
        """Builds the function logic for the component."""
        logic = []

        if (
            isinstance(self.component, Component)
            and self.component.classname in self.logic_map.keys()
        ):
            logic_list = self.get_logic_list()

            if logic_list is not None:
                logic.extend(logic_list)

        return logic


class GraphBuilder:
    """Builds the models node graph."""

    def __init__(
        self,
        model: ZentraModel,
        attr_maps: AttributeMappings,
        content_map: MappingDict,
    ) -> None:
        self.model = model
        self.attr_maps = attr_maps
        self.content_map = content_map

    def build(self) -> ComponentNode:
        """Builds the component graph for the model and returns it as a `ComponentNode`."""
        name = self.get_name(self.model)
        attrs = self.get_attributes(self.model)
        content = self.get_content(self.model)

        return self.set_node(
            self.model,
            args={
                "name": name,
                "attributes": attrs,
                "content": content,
            },
        )

    def get_name(self, model: ZentraModel) -> str:
        """Identifies the name of the model based on its type."""
        if isinstance(model, LucideIcon):
            return model.name

        return model.container_name

    def get_attributes(self, model: ZentraModel) -> str:
        """Retrieves the attributes from the `AttributeBuilder` and converts them to a string."""
        builder = AttributeBuilder(
            component=model,
            common_mapping=self.attr_maps.common,
            component_mapping=self.attr_maps.model,
        )

        return compress(builder.build(), chars=" ")

    def __get_content(self, model: ZentraModel) -> list[ZentraModel | str]:
        """Retrieves the content for the model from the `ContentBuilder`."""
        builder = ContentBuilder(model=model, mapping=self.content_map)
        return builder.build()

    def get_content(self, model: ZentraModel) -> list[ComponentNode]:
        """Identifies the type of content for the model and assigns it accordingly."""
        content = self.__get_content(model)

        if len(content) == 1:
            return self.set_node(content[0])

        return [self.set_node(model) for model in content]

    def set_node(self, model: ZentraModel, args: dict = None) -> ComponentNode:
        """Create a component node model based on the model type."""
        if isinstance(model, str):
            return StringNode(content=text_content(model))

        content = self.get_content(model) if model.content_attributes else ""

        if args is None:
            args = {
                "name": self.get_name(model),
                "attributes": self.get_attributes(model),
                "content": content,
            }

        if isinstance(model, LucideIcon):
            return IconNode(**args)
        elif isinstance(model, HTMLTag):
            return HTMLNode(**args)
        elif isinstance(model, JSIterable):
            return JSNode(
                name=model.obj_name,
                attributes=model.param_name,
                content=content,
            )
        else:
            return ComponentNode(**args)
