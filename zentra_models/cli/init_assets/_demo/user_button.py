from zentra_models.core import Block
from zentra_models.ui.control import Button


user_btn = Block(
    name="UserButton",
    components=[
        Button(
            content="Click me!",
            variant="destructive",
        )
    ],
)
