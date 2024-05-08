from cli.conf.storage import ComponentDetails
from cli.templates.builders import FORM_SCHEMA_BASE, JSX_BASE
from cli.templates.builders.model import ComponentBuilder
from cli.templates.mappings import JSXMappings
from cli.templates.storage import JSXComponentContentStorage, JSXPageContentStorage
from zentra.core import Component, Page


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
