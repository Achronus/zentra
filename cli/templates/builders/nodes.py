from typing import Optional, Self


class ComponentNode:
    """
    A tree node representing a single Zentra component model.

    Parameters:
    - `name` (`string`) - the name of the node (JSX component or HTML tag)
    - `content` (`list[ComponentNode | string], optional`) - a list of child tree nodes and/or a string of text. `None` by default
    - `attributes` (`string, optional`) - a string of attributes for the node. `None` by default
    """

    def __init__(
        self,
        name: str,
        content: Optional[list[Self] | str] = None,
        attributes: Optional[str] = None,
    ) -> None:
        self.name = name
        self.content = content if content else []
        self.attributes = f" {attributes}" if attributes else ""

    def add_child(self, child: Self) -> None:
        """Add a child child node to the content."""
        self.content.append(child)

    def simple_str(self, indent: int) -> str:
        """A string of JSX without content a self closing tag."""
        return f"{indent}<{self.name}{self.attributes} />"

    def full_str(self, indent: str = "", content: str = None) -> str:
        """A string of JSX with content and an opening and closing tag."""
        if content is None:
            content = self.content

        return f"{indent}<{self.name}{self.attributes}>{content}</{self.name}>"

    def __repr__(self) -> str:
        return f"'{self.full_str(content=self.content)}'"


class IconNode(ComponentNode):
    """A tree node representation a single Zentra icon component model."""

    def __init__(
        self,
        name: str,
        content: Optional[str] = None,
        attributes: Optional[str] = None,
    ) -> None:
        super().__init__(name, content, attributes)
        self.content = f" {content}" if content else ""

    def full_str(self, indent: str = "", content: str = None) -> str:
        """A string of JSX with content to the right of the icon."""
        if content is None:
            content = self.content

        return f"{indent}<{self.name}{self.attributes} />{content}"
