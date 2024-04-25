import re

from cli.conf.format import name_from_camel_case
from cli.conf.storage import ComponentDetails
from cli.templates.mappings import JSXMappings
from cli.templates.ui.content import text_content
from zentra.core import Component, Page
from zentra.core.base import HTMLTag, JSIterable
from zentra.core.html import Div, FigCaption, Figure
from zentra.nextjs import NextJs
from zentra.ui import Form
from zentra.ui.control import Button, IconButton, InputOTP

from pydantic import BaseModel


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


class JSXListContentStorage(BaseModel):
    """
    A storage container for the pieces of multiple JSX Zentra `Component` models.

    Parameters:
    - `imports` (`list[string]`) - a list of strings representing the components import statements
    - `logic` (`list[string]`) - a list of strings representing the component function logic
    - `content` (`list[string]`) - a list of strings containing the JSX content used in the return statement
    """

    imports: list[str] = []
    logic: list[str] = []
    content: list[str] = []


class JSXComponentContentStorage(BaseModel):
    """
    A storage container for the pieces of a JSX Zentra `Component` model.

    Parameters:
    - `imports` (`string`) - a string representing the components import statements
    - `logic` (`string`) - a string representing the component function logic
    - `attributes` (`string`) - a string representing the attributes used in the main component
    - `content` (`string`) - a string containing the JSX content used in the return statement
    """

    imports: str = ""
    logic: str = ""
    attributes: str = ""
    content: str = ""


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

    def compress_lucide_react(self, imports: list[str]) -> list[str]:
        """Combines `lucide-react` imports into a single statement (if applicable). Returns the updated/unedited list."""
        seen_lucide, new_imports = [], []
        lucide_base = 'import { **parts** } from "lucide-react"'

        for statement in imports:
            if "lucide-react" in statement:
                icon = statement.split(" ")[2]
                if icon not in seen_lucide:
                    seen_lucide.append(icon)
            else:
                new_imports.append(statement)

        if len(seen_lucide) > 0:
            parts = ", ".join(seen_lucide)
            lucide_base = lucide_base.replace("**parts**", parts)
            new_imports.append(lucide_base)
            return new_imports

        return imports

    def group_imports(self, imports: list[str]) -> list[str]:
        """Splits import statements into groups for better readability. Returns an updated import list."""
        non_components, components = [], []

        for statement in imports:
            if "@/components" not in statement:
                non_components.append(statement)
            else:
                components.append(statement)

        if len(non_components) > 0:
            non_components.append("")
            return non_components + components

        return imports

    def compress(self, values: list[str]) -> str:
        """Compresses values into a string."""
        return "\n".join(values)

    def dedupe(self, values: list[str]) -> list[str]:
        """Filters out duplicate values from the list."""
        result = list(set(values))
        result.sort()
        return result

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
        imports = self.compress_lucide_react(imports)
        imports = self.group_imports(self.dedupe(imports))
        return self.compress(imports)

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


class ParentComponentBuilder:
    """A builder for creating Zentra `Component` model JSX for components that have other components inside of them."""

    def __init__(
        self,
        component: Component,
        mappings: JSXMappings,
        details_dict: dict[str, ComponentDetails],
    ) -> None:
        self.component = component
        self.mappings = mappings
        self.details = details_dict
        self.storage = JSXListContentStorage()
        self.str_storage = JSXComponentContentStorage()

        self.inner_content = []

    def build(self) -> None:
        """Builds the JSX for the component."""
        storage = self.build_component_model(model=self.component)
        self.storage.content = storage.content.split("\n")

        if not isinstance(self.component.content, str):
            self.build_inner_content(model=self.component.content, root=True)

            content = storage.content.split("\n")
            self.storage.content = [
                content[0],
                *self.inner_content,
                *content[1:],
            ]

        self.fill_str_storage(storage=storage)

    def compress(self, values: list[str]) -> str:
        """Compresses values into a string."""
        return "\n".join(values)

    def dedupe(self, values: list[str]) -> list[str]:
        """Filters out duplicate values from the list."""
        result = list(set(values))
        result.sort()
        return result

    def fill_str_storage(self, storage: JSXComponentContentStorage) -> None:
        """Fills `self.str_storage` with the required values."""
        self.str_storage.content = self.compress(self.storage.content)
        self.str_storage.attributes = storage.attributes
        self.str_storage.imports = self.compress(self.dedupe(self.storage.imports))
        self.str_storage.logic = self.compress(self.storage.logic).strip("\n")

    def build_inner_content(
        self, model: JSIterable | HTMLTag | Component, root: bool = False
    ) -> None:
        """Extracts the inner models from the component and returns them as a list."""
        if root:
            self.handle_build_start(model=model)

        if isinstance(model, HTMLTag):
            if not model.shell:
                self.inner_content.extend(self.build_html(model=model))

        if isinstance(model, Component):
            content = [self.build_component_model(model=model).content]
            self.inner_content.extend(content)

        if hasattr(model, "content") and isinstance(model.content, Div):
            self.handle_div_shell(model_content=model.content)

        if hasattr(model, "items"):
            for item in model.items:
                if isinstance(item, HTMLTag):
                    self.inner_content.extend(self.build_html(model=item))

                elif isinstance(item, JSIterable):
                    self.build_js_iterable(model=item)

                elif isinstance(item, Component):
                    content = [self.build_component_model(model=item).content]
                    self.inner_content.extend(content)

        if root:
            self.handle_build_end(model=model)

    def handle_build_start(self, model: HTMLTag | Component) -> None:
        """Handles the logic for the root object. Configuring the required tag at the start of the build if required."""
        if isinstance(model, Div):
            if model.shell:
                self.inner_content.append("<>")

    def handle_build_end(self, model: HTMLTag | Component) -> None:
        """Handles the logic for the root object. Configuring the required tag at the end of the build if required."""
        if isinstance(model, Div):
            if model.shell:
                self.inner_content.append("</>")
            else:
                self.inner_content.append(f"</{model.classname}>")

    def handle_div_shell(self, model_content: Div) -> None:
        """Handles the logic for the Div model `shell` attribute."""
        if model_content.shell:
            self.inner_content.append("<>")
            self.build_inner_content(model=model_content)
            self.inner_content.append("</>")
        else:
            self.build_inner_content(model=model_content)

    def build_html(self, model: HTMLTag) -> list[str]:
        """Builds the content for HTMLTag models and returns them as a list of strings."""
        content, attributes = self.build_html_model(model=model)
        return self.html_content_container(
            model=model, content=content, attributes=attributes
        )

    def build_js_iterable(self, model: JSIterable) -> None:
        """Builds the content for JSIterable models and adds it to `self.inner_content`."""
        self.inner_content.append(
            "{" + f"{model.obj_name}.{model.classname}(({model.param_name}) => ("
        )
        self.build_inner_content(model=model)
        self.inner_content.append("))}")

    def build_html_model(self, model: HTMLTag) -> list[str]:
        """Builds the content of the HTML and JS model and returns it as a list of strings."""
        builder = HTMLContentBuilder(
            tag=model,
            mappings=self.mappings,
        )
        return builder.build()

    def build_component_model(self, model: Component) -> JSXComponentContentStorage:
        """Builds the component model and returns the values and adds them to `self.storage`."""
        builder = ComponentBuilder(
            component=model,
            mappings=self.mappings,
            details=self.details[model.classname],
        )
        builder.build()
        self.populate_storage(comp_store=builder.storage)

        return builder.storage

    def html_content_container(
        self, model: HTMLTag, content: list[str], attributes: list[str]
    ) -> list[str]:
        """Performs content container wrapping for HTMLTags."""
        wrapped_content = [f"<{model.classname} {attributes}>"]

        if len(content) > 0:
            wrapped_content.extend(
                [
                    *content,
                    f"</{model.classname}>",
                ]
            )

        return wrapped_content

    def populate_storage(self, comp_store: JSXComponentContentStorage) -> None:
        """Adds component items to storage."""
        for key in self.storage.__dict__.keys():
            if hasattr(comp_store, key):
                getattr(self.storage, key).append(getattr(comp_store, key))


class NextJSComponentBuilder:
    """A builder for creating Zentra `NextJS` models as JSX."""

    def __init__(self, component: Component, mappings: JSXMappings) -> None:
        self.component = component
        self.maps = mappings

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(mappings=mappings, component=component)
        self.content = ContentBuilder(component=component, mappings=mappings)

    def build(self) -> None:
        """Builds the JSX for the component."""
        self.storage.imports = self.compress(self.imports())
        self.storage.attributes = self.compress(self.attrs.build(), chars=" ")
        self.storage.content = self.compress(
            self.apply_content_containers(content=self.content.build())
        )

    def imports(self) -> list[str]:
        """Builds the imports based on the component attributes and mappings."""
        imports = [self.core_import()]
        extra_imports = self.additional_imports()

        if extra_imports:
            imports.extend(extra_imports)

        return imports

    def core_import(self) -> str:
        """Creates the core import statement for the component."""
        name = self.component.classname
        return f"import {name} from 'next/{name.lower()}'"

    def additional_imports(self) -> list[str]:
        """Creates the additional imports needed for the component."""
        results = []
        for item in self.maps.additional_imports:
            comp_type, attr_name, imports = item
            if isinstance(self.component, comp_type):
                if attr_name == "all":
                    result = imports(self.component)
                else:
                    value = getattr(self.component, attr_name)
                    result = imports(value)

                if result:
                    results.extend(result)

        if len(results) == 0:
            return None

        return results

    def apply_content_containers(self, content: list[str]) -> list[str]:
        """Wraps the components content in its outer shell and any additional wrappers (if applicable)."""
        wrapped_content = [f"<{self.component.classname} {self.storage.attributes} />"]

        if len(content) > 0:
            wrapped_content[0] = wrapped_content[0].replace(" />", ">")
            wrapped_content.extend(
                [
                    *content,
                    f"</{self.component.classname}>",
                ]
            )

        if self.component.classname in self.maps.wrappers.keys():
            wrapped_content = [
                f"<div {self.maps.wrappers[self.component.classname]}>",
                *wrapped_content,
                "</div>",
            ]

        return wrapped_content

    def compress(self, items: list[str], chars: str = "\n") -> str:
        """Concatenates a list of strings into a single string based on the given chars."""
        return chars.join([item for item in items if item])


class HTMLContentBuilder:
    """A builder for creating Zentra `HTML` model content as JSX."""

    def __init__(self, model: HTMLTag, mappings: JSXMappings) -> None:
        self.model = model
        self.maps = mappings

        self.comp_storage = JSXComponentContentStorage()
        self.multi_comp_storage = JSXListContentStorage()
        self.inner_content = []

    def build(
        self, model: HTMLTag = None, details: ComponentDetails = None
    ) -> list[str]:
        """Builds a single item's content and returns it as a list of strings."""
        if model is None:
            model = self.model

        if hasattr(model, "text"):
            self.handle_text(text=model.text)
            model.text = self.inner_content

        if isinstance(model, Div):
            self.build_div_model(item=model.items, details=details)
            model.items = self.inner_content

        if isinstance(model, Figure):
            return self.build_figure_model(model=model)

        return self.get_content(model=model)

    def build_figure_model(self, model: Figure) -> list[str]:
        """Builds the content for the Figure model and returns it as a list of strings."""
        content = []
        shell_start, shell_end = self.get_content(model=model)

        nextjs = NextJSComponentBuilder(component=model.img, mappings=self.maps)
        nextjs.build()
        self.comp_storage = nextjs.storage
        img_content = [nextjs.storage.content]

        content.append(shell_start)

        if model.img_container_styles:
            img_content.insert(0, f'<div className="{model.img_container_styles}"')
            img_content.append("</div>")

        content.extend(img_content)
        content.extend(self.build(model=model.caption))
        content.append(shell_end)
        return content

    def build_div_model(
        self,
        item: str
        | Component
        | JSIterable
        | list[str | HTMLTag | Component | JSIterable],
        details: ComponentDetails,
    ) -> None:
        """Builds the content for the Div model and stores the content in `self.inner_content` and any component information in `self.multi_comp_storage`."""
        if isinstance(item, JSIterable):
            builder = JSIterableContentBuilder(model=item, mappings=self.maps)
            self.inner_content.extend(builder.build())

        elif isinstance(item, Component):
            builder = ComponentBuilder(
                component=item, mappings=self.maps, details=details
            )
            builder.build()
            self.add_to_storage(builder.storage)
            self.inner_content.extend(builder.storage.content.split("\n"))

        elif isinstance(item, HTMLTag):
            self.inner_content.extend(self.get_content(model=item))

        elif isinstance(item, str):
            self.handle_text(text=item)

        elif isinstance(item, list):
            for i in item:
                self.build_div_model(item=i, details=details)

    def handle_text(self, text: str | HTMLTag | list[str | HTMLTag]) -> None:
        """Handles the content building for the text attribute and stores it in `self.inner_content`."""
        if isinstance(text, list):
            for item in text:
                self.handle_text(text=item)

        if isinstance(text, HTMLTag):
            self.inner_content.extend(self.get_content(model=text))
        elif isinstance(text, str):
            self.inner_content.append(text_content(text)[0])

    def get_content(self, model: HTMLTag) -> list[str]:
        """A helper function to build the content of the HTMLTag and returns it as a list of strings."""
        attr_builder = AttributeBuilder(component=model, mappings=self.maps)
        content_builder = ContentBuilder(component=model, mappings=self.maps)

        attributes = " ".join(attr_builder.build())
        content = content_builder.build()
        return self.html_content_container(
            model=model, content=content, attributes=attributes
        )

    def html_content_container(
        self, model: HTMLTag, content: list[str], attributes: list[str]
    ) -> list[str]:
        """Performs content container wrapping for HTMLTags."""
        wrapped_content = [
            f"<{model.classname}{f" {attributes}" if attributes else ''}>"
        ]

        if len(content) > 0:
            wrapped_content.extend(content)

        wrapped_content.append(f"</{model.classname}>")

        if isinstance(model, Div):
            if model.shell:
                wrapped_content[0] = "<>"
                wrapped_content[-1] = "</>"

        return wrapped_content

    def add_to_storage(self, comp_store: JSXComponentContentStorage) -> None:
        """Adds the JSX component items to `self.multi_comp_storage`."""
        self.multi_comp_storage.imports.append(comp_store.imports)
        self.multi_comp_storage.logic.append(comp_store.logic)
        self.multi_comp_storage.content.append(comp_store.content)


class JSIterableContentBuilder:
    """A builder for creating Zentra `JSIterable` model content as JSX."""

    def __init__(self, model: JSIterable, mappings: JSXMappings) -> None:
        self.model = model
        self.maps = mappings
        self.comp_storage = JSXComponentContentStorage()

    def build(self, details: ComponentDetails = None) -> list[str]:
        """Builds the content for the JSX iterable and returns it as a list of strings. If the the content inside is a component, also stores its information in `self.storage`."""
        start, end = self.get_container()

        if isinstance(self.model.content, HTMLTag):
            builder = HTMLContentBuilder(model=self.model.content, mappings=self.maps)
            content = builder.build()
            self.comp_storage = builder.comp_storage

        elif isinstance(self.model.content, NextJs):
            builder = NextJSComponentBuilder(
                component=self.model.content, mappings=self.maps
            )
            builder.build()
            content = builder.storage.content.split("\n")
            self.comp_storage = builder.storage

        else:
            try:
                builder = ComponentBuilder(
                    component=self.model.content, mappings=self.maps, details=details
                )
            except AttributeError:
                raise AttributeError(
                    f"'JSIterableContentBuilder.build(details=None)'. Missing 'ComponentDetails' for provided '{self.model.content.classname}' Component",
                )

            builder.build()
            content = builder.storage.content.split("\n")
            self.comp_storage = builder.storage

        return [start, *content, end]

    def get_container(self) -> tuple[str, str]:
        """Creates the outer shell of the iterable and returns it in the form of `(start, end)`."""
        start = (
            "{"
            + f"{self.model.obj_name}.{self.model.classname}(({self.model.param_name}) => ("
        )
        end = "))}"
        return start, end


class ComponentBuilder:
    """A builder for creating Zentra `Component` models as JSX."""

    def __init__(
        self, component: Component, mappings: JSXMappings, details: ComponentDetails
    ) -> None:
        self.component = component
        self.details = details
        self.maps = mappings

        self.storage = JSXComponentContentStorage()
        self.attrs = AttributeBuilder(component=component, mappings=mappings)
        self.imports = ImportBuilder(
            component=component,
            mappings=mappings,
            child_names=details.child_names,
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

        if len(content) > 0:
            wrapped_content[0] = wrapped_content[0].replace(" />", ">")
            wrapped_content.extend(
                [
                    *content,
                    f"</{self.component.classname}>",
                ]
            )

        if self.component.classname in self.maps.wrappers.keys():
            wrapped_content = [
                f"<div {self.maps.wrappers[self.component.classname]}>",
                *wrapped_content,
                "</div>",
            ]

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

    def __init__(self, component: Component, mappings: JSXMappings) -> None:
        self.component = component
        self.maps = mappings

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
                if attr_name == "all":
                    value = condition(self.component)
                else:
                    value = getattr(self.component, attr_name)
                    value = condition(value)

                if value:
                    attrs.extend(value)
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
        results = []
        for item in self.maps.additional_imports:
            comp_type, attr_name, imports = item
            if isinstance(self.component, comp_type):
                if attr_name == "all":
                    result = imports(self.component)
                else:
                    value = getattr(self.component, attr_name)
                    result = imports(value)

                if result:
                    results.extend(result)

        if len(results) == 0:
            return None

        return results

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
                            content.extend(self.handle_icon_button(text=content_str))
                        else:
                            content.append(content_str)

        for comp_type, condition in self.maps.component_content:
            if isinstance(self.component, comp_type):
                content_str = condition(self.component)
                if content_str:
                    content.extend(content_str)

        if len(content) > 0 and isinstance(content[0], list):
            return self.handle_single_quotes(*content)

        return self.handle_single_quotes(content)

    def handle_icon_button(self, text: list[str]) -> list[str]:
        """Handles the logic for the icon button."""
        component: IconButton = self.component
        result = []

        icon_html = f'<{component.icon} className="mr-2 h-4 w-4"/>'
        if component.icon_position == "start":
            result.extend([icon_html, *text])
        else:
            result.extend([*text, icon_html])

        if component.url:
            result.insert(0, f'<Link href="{component.url}">')
            result.append("</Link>")

        return result

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

    def handle_single_quotes(self, content: list[str]) -> list[str]:
        """Checks for `'` in a content list. If the item is a string without JSX tags, it will update the text into a suitable format for JSX processing. Returns the updated content list or unmodified version."""
        single_quote_pattern = re.compile(r"\b\w*'\w*\b")

        for idx, line in enumerate(content):
            sq_matches = single_quote_pattern.findall(line)

            if sq_matches:
                for match in sq_matches:
                    wrapped = "{`" + match + "`}"
                    content[idx] = re.sub(
                        r"\b" + re.escape(match) + r"\b", wrapped, line
                    )

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
