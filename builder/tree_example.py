from typing import Optional, Self


class JSXTreeNode:
    """
    A tree node representing a single JSX component.

    Parameters:
    - `name` (`string`) - the name of the node (JSX component or HTML tag)
    - `content` (`list[JSXTreeNode | string], optional`) - a list of child tree nodes and/or a string of text. `None` by default
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
        self.attributes = attributes if attributes else ""

    def add_child(self, child: Self) -> None:
        """Add a child child node to the content."""
        self.content.append(child)


class ParentModel(JSXTreeNode):
    """A representation of a parent JSX component."""

    def __init__(
        self,
        name: str,
        content: Optional[list[JSXTreeNode] | str] = None,
        attributes: Optional[str] = None,
    ) -> None:
        super().__init__(name, content, attributes)


class ChildModel(JSXTreeNode):
    """A representation of a child JSX component."""

    def __init__(
        self,
        name: str,
        content: Optional[list[JSXTreeNode] | str] = None,
        attributes: Optional[str] = None,
    ) -> None:
        super().__init__(name, content, attributes)


def generate_jsx(node: JSXTreeNode, level: int = 0) -> str:
    """Builds the JSX from the tree nodes."""

    def full_str(indent: int, name: str, attributes: str, content: str) -> str:
        return f"{indent}<{name}{attributes}>{content}</{name}>"

    def single_str(indent: int, name: str, attributes: str) -> str:
        return f"{indent}<{name}{attributes} />"

    indent = "  " * level
    attributes = f" {node.attributes}" if node.attributes else ""

    if isinstance(node.content, str):
        return full_str(indent, node.name, attributes, content=node.content)
    elif not node.content:
        return single_str(indent, node.name, attributes)

    children = "\n".join(
        generate_jsx(child, level + 1)
        for child in node.content
        if isinstance(child, JSXTreeNode)
    )

    return full_str(indent, node.name, attributes, content=f"\n{children}\n{indent}")


ddm = ParentModel(
    name="DropdownMenu",
    content=[
        ParentModel(
            name="DropdownMenuTrigger",
            content=[
                ChildModel(
                    name="Button",
                    attributes='variant="outline"',
                    content="Open",
                ),
            ],
            attributes="asChild",
        ),
        ParentModel(
            name="DropdownMenuContent",
            attributes='className="w-56"',
            content=[
                ChildModel(
                    name="DropdownMenuLabel",
                    content="My Account",
                ),
                ChildModel(name="DropdownMenuSeparator"),
                ParentModel(
                    name="DropdownMenuGroup",
                    content=[
                        ParentModel(
                            name="DropdownMenuItem",
                            content=[
                                ChildModel(
                                    name="User",
                                    attributes='className="mr-2 h-4 w-4"',
                                ),
                                ChildModel(name="span", content="Profile"),
                                ChildModel(name="DropdownMenuShortcut", content="⇧⌘P"),
                            ],
                        ),
                        ParentModel(
                            name="DropdownMenuItem",
                            content=[
                                ChildModel(
                                    name="CreditCard",
                                    attributes='className="mr-2 h-4 w-4"',
                                ),
                                ChildModel(name="span", content="Billing"),
                                ChildModel(name="DropdownMenuShortcut", content="⌘B"),
                            ],
                        ),
                        ParentModel(
                            name="DropdownMenuItem",
                            content=[
                                ChildModel(
                                    name="Settings",
                                    attributes='className="mr-2 h-4 w-4"',
                                ),
                                ChildModel(name="span", content="Settings"),
                                ChildModel(name="DropdownMenuShortcut", content="⌘S"),
                            ],
                        ),
                        ParentModel(
                            name="DropdownMenuItem",
                            content=[
                                ChildModel(
                                    name="Keyboard",
                                    attributes='className="mr-2 h-4 w-4"',
                                ),
                                ChildModel(name="span", content="Keyboard shortcuts"),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


jsx_content = generate_jsx(ddm)
print(jsx_content)
