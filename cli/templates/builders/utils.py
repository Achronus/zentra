from cli.templates.builders.jsx import AttributeBuilder, ContentBuilder
from cli.templates.mappings import JSXMappings
from zentra.core.base import HTMLTag
from zentra.core.html import Div


def get_html_content(model: HTMLTag, mappings: JSXMappings) -> list[str]:
    """A helper function to build the content of a HTMLTag and returns it as a list of strings."""
    attr_builder = AttributeBuilder(
        component=model,
        common_mapping=mappings.common_attrs,
        component_mapping=mappings.component_attrs,
    )
    content_builder = ContentBuilder(
        model=model,
        model_mapping=mappings.component_content,
        common_mapping=mappings.common_content,
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
        if model.shell:
            wrapped_content[0] = "<>"
            wrapped_content[-1] = "</>"

    return wrapped_content
