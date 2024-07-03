import os

from zentra_models.cli.constants.filepaths import GENERATE_PATHS
from zentra_models.cli.local.files import make_directories, remove_files
from zentra_models.cli.utils.format import name_to_camel_case
from zentra_models.cli.local.storage import ModelFileStorage
from zentra_models.cli.constants.types import LibraryNamePairs
from zentra_models.cli.templates import ComponentFileType

from zentra_models.core.enums.ui import LibraryType
from zentra_models.uploadthing import Uploadthing


class LocalBuilder:
    """
    Handles functionality for creating files and directories in the Zentra generate folder.
    """

    def __init__(self) -> None:
        self.components = ModelFileStorage()

        self.ut = Uploadthing(core_folder=os.path.basename(GENERATE_PATHS.LIB))

    def folders(self, pairs: LibraryNamePairs) -> list[str]:
        """Returns a list of `library_name` folders from a list of `LibraryNamePairs`."""
        return list(set(item[0] for item in pairs))

    def make_dirs(self) -> None:
        """Creates the needed directories inside the generate folder."""
        for dir in self.folders(self.components.generate):
            make_directories(os.path.join(GENERATE_PATHS.COMPONENTS, dir))

    def create_base_files(self, file_type: ComponentFileType) -> None:
        """
        Creates the base files for Zentra models that need to be generated in the generate folder.

        Parameter:
        - `file_type` (`string`) - the type of file to extract. Options: ['base', 'templates', 'lib']
        """
        pass

    def remove_models(self) -> None:
        """Removes a list of Zentra models from the generate folder."""
        remove_files(pairs=self.components.remove, dirpath=GENERATE_PATHS.COMPONENTS)

        if LibraryType.UPLOADTHING.value in self.folders(self.components.remove):
            core_pairs = self.ut.core_file_pairs()
            remove_files(
                pairs=core_pairs, dirpath=GENERATE_PATHS.lib, ignore_pair_folder=True
            )

    def extract_child_components(self, lines: list[str], filename: str) -> list[str]:
        """Extracts the child components from the last line a list of code content."""

        def sanitise_children(children: list[str], filename: str) -> list[str]:
            """Filters out items starting with a lowercase letter and the component name. In some Shadcn/ui components, the export line contains values such as, `buttonVariants`, `type CarouselApi`, `useFormField`, and `navigationMenuTriggerStyle`.

            These need to be filtered out before passed into the import statements.
            """
            if len(children) > 0:
                children = [item for item in children if not item[0].islower()]
                children.remove(name_to_camel_case(filename))
            return children

        def get_children(lines: list[str]) -> list[str]:
            """Extracts the child component names as a list from a given set of lines."""
            idx = [idx for idx, line in enumerate(lines) if "export {" in line][0]
            export_line = lines[idx:]

            if isinstance(export_line, list):
                export_line = " ".join(export_line)

            children = (
                export_line.replace("export", "")
                .replace("{", "")
                .replace(";", "")
                .replace("}", "")
                .replace(" ", "")
                .split(",")
            )
            return [child for child in children if child != ""]

        return sanitise_children(children=get_children(lines=lines), filename=filename)
