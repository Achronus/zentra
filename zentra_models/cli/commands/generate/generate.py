import os
from pathlib import Path
import shutil
import typer

from zentra_models.cli.commands.base import status
from zentra_models.cli.commands.base.controller import BaseController

from zentra_models.cli.constants import GenerateSuccessCodes
from zentra_models.cli.constants.filepaths import (
    GENERATE_PATHS,
    LIBRARY_FILE_MAPPING,
    LOCAL_FILES,
)

from zentra_models.cli.local.files import remove_files
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
        self.libraries = self.zentra.storage.get_name_option("libraries")

        self.counts = CountStorage()

        react_str = "[cyan]React[/cyan]"
        zentra_str = "[magenta]Zentra[/magenta]"

        tasks = [
            (self.detect_models, f"Detecting {zentra_str} models"),
            (self.retrieve_assets, "Adding core [yellow]component[/yellow] assets"),
            (self.remove_models, f"Removing unused {zentra_str} models"),
            # (self.add_zentra_files, f"Creating {react_str} files"),
        ]

        BaseController.__init__(self, tasks)

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
        all_comps = self.zentra.storage.all_components
        existing = self.get_names(all_comps, already_exist)
        generate = self.get_names(all_comps, to_generate)
        remove = self.get_names(all_comps, to_remove)
        return existing, generate, remove

    def add_library_core_files(
        self, local: list[Path], package: list[Path]
    ) -> tuple[list[Path], list[Path]]:
        """Adds the core file local and package paths for libraries if they are required."""
        for key in self.libraries:
            local, package = LIBRARY_FILE_MAPPING[key].add_core_paths(local, package)

        return local, package

    def get_library_core_files(self, root_path: Path) -> None:
        """Removes core files from libraries when their directories are empty."""
        comp_dirs = os.listdir(root_path)

        core_paths = []
        for dir in comp_dirs:
            if len(os.listdir(Path(root_path, dir))) == 0:
                paths = LIBRARY_FILE_MAPPING[dir].create_local_paths(ignore=["base"])
                core_paths.append(Path(root_path, dir))
                core_paths.extend(paths)

        return core_paths

    @status
    def detect_models(self) -> None:
        """Detects the user defined Zentra models and prepares them for file generation."""
        target_comps = self.zentra.storage.get_target_components()
        target_paths = target_comps.local_paths()
        existing_paths = LOCAL_FILES.get_paths()

        existing, generate, remove = self.find_differences(target_paths, existing_paths)

        self.counts.fill(
            existing=existing,
            generate=generate,
            remove=remove,
        )

        if (
            self.counts.get_count("generate") == 0
            and self.counts.get_count("remove") == 0
        ):
            raise typer.Exit(code=GenerateSuccessCodes.NO_NEW_COMPONENTS)

    @status
    def retrieve_assets(self) -> None:
        """Retrieves the core component assets from the Zentra package and stores them in the Zentra generate folder."""
        if self.counts.get_count("generate") > 0:
            names = self.counts.get_items("generate")
            comps = self.zentra.storage.get_components(names, "all_components")

            package_paths = comps.package_paths()
            local_paths = comps.local_paths()
            local_paths, package_paths = self.add_library_core_files(
                local_paths, package_paths
            )

            # Make directories
            dirpaths = list({path.parent for path in local_paths})
            for path in dirpaths:
                os.makedirs(path, exist_ok=True)

            # Make files
            for src, dest in zip(package_paths, local_paths):
                if not os.path.exists(dest):
                    shutil.copyfile(src, dest)

    @status
    def remove_models(self) -> None:
        """Removes files from the Zentra generate folder that are no longer needed."""
        if self.counts.get_count("remove") > 0:
            # Get existing paths
            existing_names = self.counts.get_items("existing")
            existing_comps = self.zentra.storage.get_components(
                existing_names, "all_components"
            )
            keep_paths = existing_comps.local_paths()

            # Get remove paths
            remove_names = self.counts.get_items("remove")
            remove_comps = self.zentra.storage.get_components(
                remove_names, "all_components"
            )
            remove_paths = remove_comps.local_paths()

            # Compare two - remove only ones not needed
            remove_paths = list(set(remove_paths) - set(keep_paths))
            remove_files(remove_paths)

            # Cleanup core files when empty directories
            core_paths = self.get_library_core_files(GENERATE_PATHS.COMPONENTS)
            remove_files(core_paths)

    @status
    def add_zentra_files(self) -> None:
        """Builds the React files based on the information in the Zentra app."""
        pass
