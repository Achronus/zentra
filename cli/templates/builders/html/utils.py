from cli.templates.builders.jsx import AttributeBuilder, ContentBuilder
from cli.templates.ui.mappings.storage import HTMLShellMappings
from zentra.core.base import HTMLTag
from zentra.core.html import Div


def get_html_content(model: HTMLTag, mappings: HTMLShellMappings) -> list[str]:
    """A helper function to build the content of a HTMLTag and returns it as a list of strings."""
    attr_builder = AttributeBuilder(
        component=model,
        common_mapping=mappings.attribute.common,
        component_mapping=mappings.attribute.model,
    )
    content_builder = ContentBuilder(
        model=model,
        model_mapping=mappings.content.model,
        common_mapping=mappings.content.common,
    )

    attributes = " ".join(attr_builder.build())
    content = content_builder.build()
    return html_content_container(model=model, content=content, attributes=attributes)


def html_content_container(
    model: HTMLTag, content: list[str], attributes: list[str]
) -> list[str]:
    """A helper function for wrapping content in the correct HTML container."""
    wrapped_content = [f"<{model.classname}{f" {attributes}" if attributes else ''}>"]

    if len(content) > 0:
        wrapped_content.extend(content)

    wrapped_content.append(f"</{model.classname}>")

    if isinstance(model, Div):
        if model.fragment:
            wrapped_content[0] = "<>"
            wrapped_content[-1] = "</>"

    return wrapped_content
