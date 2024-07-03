from zentra_models.cli.commands.base import status
from zentra_models.cli.commands.base.controller import BaseController

from zentra_models.cli.local.storage import ModelFileStorage, ModelStorage
from zentra_models.cli.constants.types import LibraryNamePairs

from zentra_models.cli.local.builder import LocalBuilder
from zentra_models.cli.local.extractor import LocalExtractor

from zentra_models.core import Zentra


class GenerateController(BaseController):
    """
    A controller for handling tasks that generate the Zentra components.

    Parameters:
    - `zentra` (`zentra.core.Zentra`) - the Zentra application containing components to generate
    """

    def __init__(self, zentra: Zentra) -> None:
        self.local_extractor = LocalExtractor(zentra.name_storage)

        self.storage = ModelStorage()
        self.local_builder = LocalBuilder()

        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (self.detect_models, f"Detecting {zentra_str} models"),
            (
                self.retrieve_assets,
                "Retrieving core [yellow]component[/yellow] assets from [yellow]GitHub[/yellow]",
            ),
            (self.remove_models, f"Removing unused {zentra_str} models"),
            (self.update_template_files, f"Configuring {react_str} components"),
        ]

        BaseController.__init__(self, tasks)

    def store_models(
        self,
        existing: LibraryNamePairs,
        add: LibraryNamePairs,
        remove: LibraryNamePairs,
    ) -> None:
        """Stores Zentra model changes in `ModelStorage`."""
        changes = {
            "existing": existing,
            "generate": add,
            "remove": remove,
            "counts": self.local_extractor.model_counts,
        }

        self.storage.components = ModelFileStorage(**changes)
        self.local_builder.components = self.storage.components

    @status
    def detect_models(self) -> None:
        """Detects the user defined Zentra models and prepares them for file generation."""
        user_models = self.local_extractor.user_models()
        existing_models = self.local_extractor.existing_models()

        self.local_extractor.no_new_components_check(user_models, existing_models)

        to_add, to_remove = self.local_extractor.model_changes(
            existing_models,
            user_models,
        )

        self.store_models(
            existing=existing_models,
            add=to_add,
            remove=to_remove,
        )

    @status
    def retrieve_assets(self) -> None:
        """Retrieves the core component assets from GitHub and stores them in the Zentra generate folder."""
        if self.storage.components.counts.generate > 0:
            self.local_builder.make_dirs()
            self.local_builder.create_base_files(file_type="base")

    @status
    def remove_models(self) -> None:
        """Removes the React component files that are no longer used from the Zentra generate folder."""
        if self.storage.components.counts.remove > 0:
            self.local_builder.remove_models()

    @status
    def update_template_files(self) -> None:
        """Updates the React components based on the Zentra model attributes."""
        pass
        # TODO: add logic for 'extract_component_details' or remove function if not needed
        # Likely better to find alternative. Function is long and slow
