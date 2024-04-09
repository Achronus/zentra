from typing import Callable

from cli.conf.format import name_from_camel_case
from cli.conf.storage import ComponentDetails
from zentra.core import Component, Page
from zentra.ui import Form
from zentra.ui.control import Button, IconButton, InputOTP

from pydantic import BaseModel


# (attribute_name, lambda_expression)
AttributeMapping = list[tuple[str, Callable]]

# (component_type, attribute_name, lambda_expression)
ComponentAttributesMapping = list[tuple[Component, str, Callable]]

FORM_SCHEMA_BASE = """
const FormSchema = z.object({
  **form_schema**
});
"""

JSX_BASE = """**imports**

type Props = {
  **props**
}
**form_schema**
const PageName = (**prop_params**: Props) => {
  **logic**
  return (
      **content**
  );
};

export default PageName;
"""


class JSXMappings(BaseModel):
    """A storage container for JSX mappings."""

    common_attrs: AttributeMapping
    component_attrs: list[tuple]
    common_content: list[tuple]
    component_content: list[tuple]
    common_logic: list[tuple]
    use_client_map: list[str]
    use_state_map: list[str]
    additional_imports: list[tuple]
    wrappers: dict[str, str]


class JSXPageContentStorage(BaseModel):
    """
    A storage container for the pieces of a JSX Zentra `Page` model.

    Parameters:
    - `imports` (`list[string]`) - a list of strings representing import statements
    - `logic` (`list[string]`) - a list of strings representing the component function logic
    - `content` (`list[string]`) - a list of strings containing the JSX content used in the return statement
    - `props` (`list[string]`) - a list of strings representing the TypeScript props
    - `form_schema` (`list[string], optional`) - a list of strings representing the form schema, if the page contains a form. `None` by default
    """

    imports: list[str] = []
    logic: list[str] = []
    content: list[str] = []
    props: list[str] = []
    form_schema: list[str] = None


class JSXComponentContentStorage(BaseModel):
    """
    A storage container for the pieces of a JSX Zentra `Component` model.

    Parameters:
    - `imports` (`list[string]`) - a list of strings representing import statements
    - `logic` (`list[string]`) - a list of strings representing the component function logic
    - `attributes` (`list[string]`) - a list of strings representing the attributes used in the main component
    - `content` (`list[string]`) - a list of strings containing the JSX content used in the return statement
    """

    imports: list[str] = []
    logic: list[str] = []
    attributes: list[str] = []
    content: list[str] = []


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
        self.use_client = False
        self.form_schema_base = FORM_SCHEMA_BASE
        self.jsx = JSX_BASE

    def get_details(self, component: Component) -> ComponentDetails:
        """Retrieves the component details for the component."""
        for details in self.component_details:
            if component.classname == details.name:
                return details

    def build(self) -> None:
        """Builds the JSX for the page."""

        for component in self.page.components:
            self.check_for_use_client(component=component)
            details = self.get_details(component=component)
            builder = ComponentBuilder(
                component=component,
                mappings=self.mappings,
                details=details,
            )
            builder.build()
            self.populate_storage(comp_store=builder.storage)

        self.fill_jsx()

        if self.use_client:
            self.jsx = f'"use_client"\n\n{self.jsx}'

    def check_for_use_client(self, component: Component) -> None:
        """Performs a check to enable `use_client` at the top of the page if any required components exist."""
        if component.classname in self.mappings.use_client_map:
            self.use_client = True

    def populate_storage(self, comp_store: JSXComponentContentStorage) -> None:
        """Adds component items to storage."""
        for key in self.storage.__dict__.keys():
            if hasattr(comp_store, key):
                getattr(self.storage, key).append(getattr(comp_store, key))

    def fill_jsx(self) -> None:
        """Concatenates the lists of JSX content into strings, removes duplicate imports and redundant logic statements, and adds them to the appropriate areas in the JSX template."""
        imports = self.set_imports(self.storage.imports)
        logic = self.set_logic(self.storage.logic)
        content = self.set_content(self.storage.content)
        form_schema = self.set_form_schema(self.storage.form_schema)
        props, prop_params = self.set_props(self.storage.props)

        self.jsx = self.jsx.replace("PageName", self.page.name)
        self.jsx = self.jsx.replace("**imports**", imports)
        self.jsx = self.jsx.replace("**logic**", logic)
        self.jsx = self.jsx.replace("**content**", content)
        self.jsx = self.jsx.replace("**form_schema**", form_schema)
        self.jsx = self.jsx.replace("**props**", props)
        self.jsx = self.jsx.replace("**prop_params**", prop_params)

    def unpack_additional_imports(self, imports_list: list[str]) -> list[str]:
        """Unpacks additional import values if a newline character is present in the list."""
        unpacked_imports = []
        for import_str in imports_list:
            if "\n" in import_str:
                unpacked_imports.extend(import_str.split("\n"))
            else:
                unpacked_imports.append(import_str)
        return unpacked_imports

    def compress(self, values: list[str]) -> str:
        """Compresses an attributes values into a string."""
        return "\n".join(values)

    def dedupe(self, values: list[str]) -> list[str]:
        """Filters out duplicate values from the list."""
        result = list(set(values))
        result.sort()
        return result

    def dedupe_n_compress(self, values: list[str]) -> str:
        """Filters out duplicate values from a list and compresses them into a single string."""
        return self.compress(self.dedupe(values))

    def set_form_schema(self, form_schema: list[str]) -> str:
        """Sets the form schema depending on if a form exists in the page. If one does, uses `form_schema_base` to populate the values and returns it. Otherwise, returns an empty string."""
        if form_schema:
            form_schema = self.compress(self.storage.form_schema)
            return self.form_schema_base.replace("**form_schema**", form_schema)
        else:
            return ""

    def set_imports(self, imports: list[str]) -> str:
        """Sets the import statements depending on the values stored in storage and returns them as a compiled string."""
        imports = self.unpack_additional_imports(imports)
        return self.dedupe_n_compress(imports)

    def set_logic(self, logic: list[str]) -> str:
        """Sets the page logic depending on the values stored in storage and returns them as a compiled string."""
        return self.compress(logic).strip("\n")

    def set_content(self, content: list[str]) -> str:
        """Sets the page JSX content depending on the values stored in storage and returns them as a compiled string."""
        content.insert(0, "<>")
        content.append("</>")
        return self.compress(content)

    def set_props(self, props: list[str]) -> tuple[str, str]:
        """Sets the prop content and prop parameters depending on the values stored in storage and returns them as a compiled string."""
        if props:
            # TODO: update logic here
            return self.compress(props), self.compress(props)
        else:
            return "", "props"


class ComponentBuilder:
    """A builder for creating Zentra `Component` models as JSX."""

    def __init__(
        self, component: Component, mappings: JSXMappings, details: ComponentDetails
    ) -> None:
        self.component = component
        self.details = details
        self.maps = mappings

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(mappings=mappings, component=component)
        self.imports = ImportBuilder(
            component=component, mappings=mappings, child_names=details.child_names
        )
        self.logic = LogicBuilder(component=component, mappings=mappings)
        self.content = ContentBuilder(component=component, mappings=mappings)

    def build(self) -> None:
        """Builds the JSX for the component."""
        self.storage.imports = self.compress(self.imports.build())
        self.storage.attributes = self.compress(self.attrs.build(), chars=" ")
        self.storage.logic = self.compress(self.logic.build())
        self.storage.content = self.compress(
            self.apply_content_containers(content=self.content.build())
        )

    def apply_content_containers(self, content: list[str]) -> list[str]:
        """Wraps the components content in its outer shell and any additional wrappers (if applicable)."""
        wrapped_content = [f"<{self.component.classname} {self.storage.attributes} />"]

        if len(content) > 1:
            wrapped_content[0] = wrapped_content[0].replace(" />", ">")
            wrapped_content.extend(
                [
                    *content,
                    f"</{self.component.classname}>",
                ]
            )

        if self.component.classname in self.maps.wrappers.keys():
            wrapped_content.extend(
                [
                    f"<div {self.maps.wrappers[self.component.classname]}>",
                    *wrapped_content,
                    "</div>",
                ]
            )
        return wrapped_content

    def compress(self, items: list[str], chars: str = "\n") -> str:
        """Concatenates a list of strings into a single string based on the given chars."""
        return chars.join([item for item in items if item])


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
                    attrs.extend(condition(value))
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
        use_state = self.use_state()
        imports = [self.core_import()]

        if use_state:
            imports.extend(use_state)

        if additional_imports:
            imports.extend(additional_imports)

        return [item for item in imports if item]

    def core_import(self) -> str:
        """Creates the core import statement for the component."""
        filename = name_from_camel_case(self.component.classname)
        return f'import {{ {self.core_import_pieces()} }} from "@/components/{self.component.library}/{filename}"'.replace(
            "'", " "
        )

    def additional_imports(self) -> list[str]:
        """Creates the additional imports needed for the component."""
        for item in self.maps.additional_imports:
            comp_type, attr_name, imports = item
            if isinstance(self.component, comp_type):
                value = getattr(self.component, attr_name)
                if value:
                    return imports(value)
        return None

    def core_import_pieces(self) -> str:
        """Creates the core import pieces including the main component and its children (if required)."""
        return ", ".join([self.component.classname] + self.child_names)

    def use_state(self) -> list[str]:
        """Adds React's `useState` import if the component requires it."""
        if self.component.classname in self.maps.use_state_map:
            return ['import { useState } from "react"']
        return None


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

                    if attr_name == "text" and not isinstance(self.component, Button):
                        if hasattr(self.component, "icon_position"):
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


class LogicBuilder:
    """A builder for creating the Zentra `Component` function logic created above the `return` statement."""

    def __init__(self, component: Component, mappings: JSXMappings) -> None:
        self.component = component
        self.maps = mappings

    def build(self) -> list[str]:
        """Builds the function logic for the component."""
        logic = []

        for item in self.maps.common_logic:
            comp_type, attr_name, condition = item
            if isinstance(self.component, comp_type):
                value = getattr(self.component, attr_name)
                if value:
                    logic.extend(condition(value))

        return logic
