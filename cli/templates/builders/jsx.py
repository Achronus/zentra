from cli.conf.format import name_from_camel_case
from cli.conf.types import MappingDict
from cli.templates.utils import handle_single_quotes, remove_none

from zentra.core import Component
from zentra.core.base import HTMLTag
from zentra.core.react import LucideIcon
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
                if isinstance(self.component, (Component, LucideIcon)):
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
        self,
        component: Component,
        additional_imports_mapping: MappingDict,
        use_state_mapping: MappingDict,
        core_name: str,
        child_names: list[str],
    ) -> None:
        self.component = component
        self.additional_map = additional_imports_mapping
        self.use_state_map = use_state_mapping
        self.core_name = core_name
        self.child_names = child_names

    def build(self) -> list[str]:
        """Builds the import statements for the component."""
        additional_imports = self.additional_imports()
        use_state = self.use_state()
        imports = [self.core_import()]

        if use_state:
            imports.extend(use_state)

        if additional_imports:
            imports.extend(additional_imports)

        return [item for item in imports if item]

    def core_import(self) -> str:
        """Creates the core import statement for the component."""
        filename = name_from_camel_case(self.core_name)
        return f'import {{ {self.core_import_pieces()} }} from "@/components/{self.component.library}/{filename}"'.replace(
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

    def core_import_pieces(self) -> str:
        """Creates the core import pieces including the main component and its children (if required)."""
        return ", ".join([self.core_name] + self.child_names)

    def use_state(self) -> list[str]:
        """Adds React's `useState` import if the component requires it."""
        if self.component.classname in self.use_state_map:
            return ['import { useState } from "react"']
        return None


class ContentBuilder:
    """A builder for creating Zentra `Component` content."""

    def __init__(
        self,
        model: Component | HTMLTag,
        model_mapping: MappingDict,
        common_mapping: MappingDict,
    ) -> None:
        self.model = model

        self.model_map = model_mapping
        self.common_map = common_mapping

    def get_common(self, attr_name: str, value: str | list[str]) -> list[str]:
        """A helper function to retrieve the content from the `common_map` for the zentra model."""
        return self.common_map[attr_name](value)

    def get_content(self) -> list[str]:
        """A helper function to retrieve the content from the `model_map` for the zentra model."""
        return self.model_map[self.model.classname](self.model)

    def build(self) -> list[str]:
        """Builds the content for the component."""
        content = []

        if isinstance(self.model, (Component, HTMLTag)):
            if self.model.classname in self.model_map.keys():
                inner_content = self.get_content()

                if inner_content is not None:
                    content.extend(inner_content)

            model_dict = self.model.__dict__
            for attr_name, value in model_dict.items():
                if (
                    value is not None
                    and attr_name in self.common_map.keys()
                    and attr_name not in self.model.custom_common_content
                ):
                    inner_content = self.get_common(attr_name, value)
                    content.extend(inner_content)

        return handle_single_quotes(content)


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
