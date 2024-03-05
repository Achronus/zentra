from .base import BaseController, status


class GenerateController(BaseController):
    """A controller for handling tasks that generate the Zentra components."""

    def __init__(self) -> None:
        tasks = []

        super().__init__(tasks)

    @status
    def retrieve_files(self) -> None:
        """Extracts the files needed based on the created Zentra models in the `models` folder."""
        pass
