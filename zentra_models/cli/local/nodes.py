from typing import Self


class ComponentNode:
    """
    A simple tree node representing a single Zentra component model.

    Parameters:
    - `name` (`string`) - the classname of the node
    - `library` (`string`) - the library the node comes from
    - `children` (`list[ComponentNode], optional`) - a list of child nodes. `[]` by default
    """

    def __init__(
        self,
        name: str,
        library: str,
        children: list[Self] = [],
    ) -> None:
        self.name = name
        self.library = library
        self.children = children

    def add_child(self, child: Self) -> None:
        """Add a child child node to the content."""
        self.children.append(child)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}', library='{self.library}', children='{self.children}')"

    def pair(self) -> tuple[str, str]:
        """Returns a tuple of the node pair."""
        return (self.library, self.name)
