import os
from pathlib import Path
import typer

from zentra_models.cli.commands.base import status
from zentra_models.cli.commands.base.controller import BaseController

from zentra_models.cli.constants import GenerateSuccessCodes
from zentra_models.cli.constants.filepaths import UI_FILES, LOCAL_FILES

from zentra_models.cli.local.storage import ComponentStorage, CountStorage
from zentra_models.core import Zentra


class GenerateController(BaseController):
    """
    A controller for handling tasks that generate the Zentra components.

    Parameters:
    - `zentra` (`zentra.core.Zentra`) - the Zentra application containing components to generate
    """

    def __init__(self, zentra: Zentra) -> None:
        self.zentra = zentra

        self.counts = CountStorage()

        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (self.detect_models, f"Detecting {zentra_str} models"),
            (
                self.retrieve_assets,
                "Retrieving core [yellow]component[/yellow] assets from [yellow]GitHub[/yellow]",
            ),
            (self.build_pages, f"Building {react_str} pages"),
            # (self.remove_models, f"Removing unused {zentra_str} models"),
            # (self.update_template_files, f"Configuring {react_str} components"),
        ]

        BaseController.__init__(self, tasks)

    @status
    def build_pages(self) -> None:
        """Creates the `frontend` pages based on the `Zentra Page` models."""
        pass

    def get_names(self, comps: ComponentStorage, paths: list[Path]) -> list[str]:
        """A helper method to return a list of names given a list of paths."""
        names = []
        for path in paths:
            filename = os.path.basename(path)
            comp = comps.get_comp_by_filename(filename)

            if comp:
                names.append(comp.name)

        names.sort()
        return names

    def find_differences(
        self, target_paths: list[Path], existing_paths: list[Path]
    ) -> tuple[list[str], list[str], list[str]]:
        """A helper method to find the differences between two sets of paths. Returns the names of as a tuple of lists in the form: `(existing, generate, remove)`."""
        target_paths = set(target_paths)
        existing_paths = set(existing_paths)

        to_generate = list(target_paths - existing_paths)
        to_remove = list(existing_paths - target_paths)
        already_exist = list(target_paths & existing_paths)

        # Get names of components based on path
        all_comps = self.zentra.storage.components
        existing = self.get_names(all_comps, already_exist)
        generate = self.get_names(all_comps, to_generate)
        remove = self.get_names(all_comps, to_remove)
        return existing, generate, remove

    @status
    def detect_models(self) -> None:
        """Detects the user defined Zentra models and prepares them for file generation."""
        target_comps = self.zentra.storage.get_target_components()
        target_paths = target_comps.local_paths()
        existing_paths = LOCAL_FILES.get_paths()

        # TODO: add 'ui' core files
        # if "ui" in self.zentra.storage.get_name_option("libraries"):
        #     target_paths.extend(UI_FILES.get_root_paths())
        #     target_paths.extend(UI_FILES.create_local_paths())

        existing, generate, remove = self.find_differences(target_paths, existing_paths)

        self.counts.fill(
            existing=existing,
            generate=generate,
            remove=remove,
        )

        if self.counts.get_count("generate") == 0:
            raise typer.Exit(code=GenerateSuccessCodes.NO_NEW_COMPONENTS)

    @status
    def retrieve_assets(self) -> None:
        """Retrieves the core component assets from GitHub and stores them in the Zentra generate folder."""
        if self.storage.components.counts.generate > 0:
            self.local_builder.make_dirs()
            self.local_builder.create_base_files()

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
