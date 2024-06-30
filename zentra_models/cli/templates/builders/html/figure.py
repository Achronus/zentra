from zentra_models.cli.templates.builders import add_to_storage
from zentra_models.cli.templates.builders.html.utils import get_html_content

from zentra_models.cli.templates.builders.nextjs import NextJSComponentBuilder
from zentra_models.cli.templates.storage import (
    JSXComponentContentStorage,
    JSXComponentExtras,
)
from zentra_models.cli.templates.ui.content import text_content

from zentra_models.cli.templates.ui.mappings.storage import (
    FigureMappings,
    HTMLShellMappings,
)
from zentra_models.cli.templates.utils import str_to_list

from zentra_models.base.html import HTMLTag
from zentra_models.core.html import FigCaption, Figure
from zentra_models.nextjs import Image


class FigureBuilder:
    """A builder for creating the `Figure` Zentra HTML model content as JSX."""

    def __init__(self, model: Figure, mappings: FigureMappings) -> None:
        self.model = model
        self.maps = mappings

        self.caption_builder = FigCaptionBuilder(
            model=model.caption,
            mappings=mappings.html_shell,
        )

        self.storage = JSXComponentExtras()

    def build_img_content(
        self, img: Image
    ) -> tuple[list[str], JSXComponentContentStorage]:
        """Creates the JSX for the `Image` model and returns its details as a tuple in the form of `(content, comp_storage)`."""
        nextjs = NextJSComponentBuilder(component=img, mappings=self.maps.nextjs)
        nextjs.build()
        return str_to_list(nextjs.storage.content), nextjs.storage

    def build(self) -> tuple[list[str], JSXComponentExtras]:
        """Builds the JSX content and returns it as a tuple in the form: `(content, storage)`."""
        content = []
        shell_start, shell_end = get_html_content(
            model=self.model,
            mappings=self.maps.html_shell,
        )

        fig_content = self.caption_builder.build()
        img_content, nextjs_storage = self.build_img_content(self.model.img)
        self.storage = add_to_storage(self.storage, nextjs_storage)

        if self.model.img_container_styles:
            img_content.insert(0, f'<div className="{self.model.img_container_styles}"')
            img_content.append("</div>")

        content.extend(img_content)
        content.extend(fig_content)

        content.insert(0, shell_start)
        content.append(shell_end)

        return content, self.storage


class FigCaptionBuilder:
    """A builder for creating the `FigCaption` Zentra HTML model content as JSX."""

    def __init__(self, model: FigCaption, mappings: HTMLShellMappings) -> None:
        self.model = model
        self.maps = mappings

    def build(self) -> list[str]:
        """Builds the JSX content and returns it as a list of strings."""
        if not isinstance(self.model.text, list):
            self.model.text = [self.model.text]

        inner_content = []
        for item in self.model.text:
            if isinstance(item, HTMLTag):
                inner_content.extend(get_html_content(item, self.maps))
            elif isinstance(item, str):
                inner_content.append(text_content(item)[0])

        self.model.text = inner_content
        return get_html_content(self.model, self.maps)
