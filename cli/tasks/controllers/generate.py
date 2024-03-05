from cli.tasks.controllers.base import BaseController, status
from cli.conf.constants import LocalUIComponentFilepaths
from cli.conf.extract import get_filenames_in_subdir
from zentra.models import zentra


class GenerateController(BaseController):
    """A controller for handling tasks that generate the Zentra components."""

    def __init__(self) -> None:
        tasks = [
            (self.extracting_models, "Retrieving [magenta]Zentra[/magenta] models"),
            (self.create_files, "Generating [cyan]React[/cyan] components"),
            (self.update_template_files, "Modifying [cyan]React[/cyan] components"),
        ]

        super().__init__(tasks)

    def _get_ui_base_filenames(self) -> list[str]:
        """Returns a list of filenames found in the `components/zentra/ui/base` folder."""
        return get_filenames_in_subdir(LocalUIComponentFilepaths.BASE)

    @status
    def extracting_models(self) -> None:
        """Extracts the zentra models and prepares them for file generation."""
        base_ui_filenames = self._get_ui_base_filenames()
        # Steps 1 to 3

    @status
    def create_files(self) -> None:
        """Creates the React components based on the extracting models."""
        pass
        # Steps 4 and 5

    @status
    def update_template_files(self) -> None:
        """Updates the React components based on the Zentra model attributes."""
        pass
        # Steps 6 to 8


# 1. [X] Get filenames from components/ui/base <- make dynamic for future libraries
# 2. [] Get components from zentra class
# 3. [] Convert component names from camelcase
# 4. [] Copy files in base that match component names to components/zentra/ui/base
# 5. [] Copy template files that match component names to components/zentra/ui/<filename>
# 6. [] Convert components to JSON
# 7. [] Update template files with information from component attributes using JSON
# 8. [] Update components/zentra/ui/index.tsx with component exports
