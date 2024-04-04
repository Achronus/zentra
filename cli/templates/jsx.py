from typing import Callable
from cli.conf.format import name_from_camel_case

from pydantic import BaseModel

from cli.conf.storage import ComponentDetails
from zentra.core import Component, Page
from zentra.ui import Form
from zentra.ui.control import IconButton, InputOTP


# (attribute_name, lambda_expression)
AttributeMapping = list[tuple[str, Callable]]

# (component_type, attribute_name, lambda_expression)
ComponentAttributesMapping = list[tuple[Component, str, Callable]]


class JSXMappings(BaseModel):
    """A storage container for JSX mappings."""

    common_attrs: AttributeMapping
    component_attrs: list[tuple]
    common_content: list[tuple]
    component_content: list[tuple]
    use_client_map: list[str]
    additional_imports: list[tuple]
    wrappers: dict[str, str]


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

    def __init__(
        self,
        page: Page,
        mappings: JSXMappings,
        component_details: list[ComponentDetails],
    ) -> None:
        self.page = page
        self.mappings = mappings
        self.component_details = component_details

        self.storage = JSXPageContentStorage()
        self.jsx = ""

    def get_details(self, component: Component) -> ComponentDetails:
        """Retrieves the component details for the component."""
        for details in self.component_details:
            if component.classname == details.name:
                return details

    def build(self) -> str:
        """Builds the JSX for the page."""

        for component in self.page.components:
            details = self.get_details(component=component)
            builder = ComponentBuilder(
                component=component,
                mappings=self.mappings,
                details=details,
            )
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


class ComponentBuilder:
    """A builder for creating Zentra `Component` models as JSX."""

    def __init__(
        self, component: Component, mappings: JSXMappings, details: ComponentDetails
    ) -> None:
        self.component = component
        self.details = details

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(mappings=mappings, component=component)
        self.imports = ImportBuilder(
            component=component, mappings=mappings, child_names=details.child_names
        )
        self.content = ContentBuilder(component=component, mappings=mappings)

    def build(self, container: JSXPageContentStorage) -> None:
        """Builds the JSX for the component."""
        self.storage.imports = self.imports.build()
        self.storage.attributes = self.attrs.build()
        self.storage.jsx = self.content.build()
        print(self.component.classname, self.storage)

    def apply_content_containers(
        self, content: list[str], wrapper_map: dict[str, str]
    ) -> list[str]:
        """Wraps the components content in its outer shell and any additional wrappers (if applicable)."""
        class_wrapper = f"<{self.component.classname}"
        if len(content) > 1:
            content.insert(0, class_wrapper)


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

    def __init__(self, mappings: JSXMappings, component: Component) -> None:
        self.maps = mappings
        self.component = component

    def build(self) -> list[str]:
        """Builds the attributes from a mapping for the component."""
        attrs = []

        for attr_name, condition in self.maps.common_attrs:
            if hasattr(self.component, attr_name):
                value = getattr(self.component, attr_name)
                if value:
                    attrs.append(condition(value))

        for item in self.maps.component_attrs:
            comp_type, attr_name, condition = item
            if isinstance(self.component, comp_type):
                value = getattr(self.component, attr_name)
                if value:
                    attrs += condition(value)
        return attrs


class ImportBuilder:
    """A builder for creating Zentra `Component` import statements."""

    def __init__(
        self, component: Component, mappings: JSXMappings, child_names: list[str]
    ) -> None:
        self.component = component
        self.maps = mappings
        self.child_names = child_names

    def build(self) -> list[str]:
        """Builds the import statements for the component."""
        additional_imports = self.additional_imports()
        imports = [self.require_client(), self.core_import()]

        if additional_imports:
            imports.extend(additional_imports)

        return [item for item in imports if item]

    def require_client(self) -> str:
        """Adds the `use_client` line to the import statement if required by the component."""
        if self.component.classname in self.maps.use_client_map:
            return '"use_client"'
        return None

    def core_import(self) -> str:
        """Creates the core import statement for the component."""
        filename = name_from_camel_case(self.component.classname)
        return f'import {{ {self.core_import_pieces()} }} from "../{self.component.library}/{filename}"'.replace(
            "'", " "
        )

    def additional_imports(self) -> list[str]:
        """Creates the additional imports needed for the component."""
        for item in self.maps.additional_imports:
            component_type, imports = item
            if isinstance(self.component, component_type):
                return imports
        return None

    def core_import_pieces(self) -> str:
        """Creates the core import pieces including the main component and its children (if required)."""
        return ", ".join([self.component.classname] + self.child_names)


class ContentBuilder:
    """A builder for creating Zentra `Component` content."""

    def __init__(self, component: Component, mappings: JSXMappings) -> None:
        self.component = component
        self.maps = mappings

    def build(self) -> list[str]:
        """Builds the content for the component."""
        content = []

        for attr_name, condition in self.maps.common_content:
            if isinstance(self.component, InputOTP):
                content.extend(self.handle_input_otp())

            elif hasattr(self.component, attr_name):
                value = getattr(self.component, attr_name)
                if value:
                    content_str = condition(value)
                    if attr_name == "text" and hasattr(self.component, "icon_position"):
                        content.extend(self.handle_icon_position(text=content_str))
                    else:
                        content.append(content_str)

        for comp_type, attr_name, condition in self.maps.component_content:
            if isinstance(self.component, comp_type):
                value = getattr(self.component, attr_name)
                if value:
                    content_str = condition(self.component)
                    content.extend(content_str)

        return content

    def handle_icon_position(self, text: str) -> list[str]:
        """Handles the logic for the content for the `icon_position` attribute."""
        component: IconButton = self.component

        icon_html = f'<{component.icon.classname} className="mr-2 h-4 w-4"/>'
        if component.icon_position == "start":
            return [icon_html, text]
        else:
            return [text, icon_html]

    def handle_input_otp(self) -> list[str]:
        """Input OTP is difficult to create with a single list comprehension. Instead, we create it separately here."""
        content = []
        component: InputOTP = self.component

        slot_group_size = component.num_inputs // component.num_groups
        slot_idx = 0

        group_tag = "InputOTPGroup>"

        for group_idx in range(component.num_groups):
            content.append(f"<{group_tag}")
            for _ in range(slot_group_size):
                content.append(f"<InputOTPSlot index={{{slot_idx}}} />")
                slot_idx += 1
            content.append(f"</{group_tag}")

            if component.num_groups > 1 and group_idx + 1 != component.num_groups:
                content.append("<InputOTPSeparator />")

        return content
