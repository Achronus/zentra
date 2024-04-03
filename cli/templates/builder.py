import os

from cli.conf.cleanup import remove_files
from cli.conf.create import make_code_file_from_url, make_directories
from cli.conf.storage import GeneratePathStorage, ModelFileStorage
from cli.conf.types import LibraryNamePairs
from cli.templates import ComponentFileType
from cli.templates.retrieval import CodeRetriever

from zentra.core.enums.ui import LibraryType
from zentra.uploadthing import Uploadthing


class LocalBuilder:
    """
    Handles functionality for creating files and directories in the Zentra generate folder.

    Parameters:
    - `url` (`string`) - a GitHub URL housing the component files
    - `paths` (`storage.GeneratePathStorage`) - a path storage container with paths specific to the controller
    - `components` (`ModelFileStorage`) - a container filled with the Zentra model pairs to `generate` and `remove`
    """

    def __init__(
        self, url: str, paths: GeneratePathStorage, components: ModelFileStorage
    ) -> None:
        self.url = url
        self.paths = paths
        self.components = components

        self.retriever = CodeRetriever(url=url)
        self.ut = Uploadthing(core_folder=os.path.basename(self.paths.lib))

    def folders(self, pairs: LibraryNamePairs) -> list[str]:
        """Returns a list of `library_name` folders from a list of `LibraryNamePairs`."""
        return list(set(item[0] for item in pairs))

    def make_dirs(self) -> None:
        """Creates the needed directories inside the generate folder."""
        for dir in self.folders(self.components.generate):
            make_directories(os.path.join(self.paths.components, dir))

    def create_base_files(self, file_type: ComponentFileType) -> None:
        """
        Creates the base files for Zentra models that need to be generated in the generate folder.

        Parameter:
        - `file_type` (`string`) - the type of file to extract. Options: ['base', 'templates', 'lib']
        """
        for folder, filename in self.components.generate:
            url = f"{self.url}/{folder}/{file_type}"
            make_code_file_from_url(
                url=url,
                filename=filename,
                dest_path=os.path.join(self.paths.components, folder),
            )

            if folder == LibraryType.UPLOADTHING.value:
                dest_path = self.paths.lib
                os.makedirs(dest_path, exist_ok=True)

                core_path, core_filenames = self.ut.core_file_urls()
                for core_filename in core_filenames:
                    make_code_file_from_url(
                        url=core_path,
                        filename=core_filename,
                        dest_path=dest_path,
                    )

    def remove_models(self) -> None:
        """Removes a list of Zentra models from the generate folder."""
        remove_files(pairs=self.components.remove, dirpath=self.paths.components)

        if LibraryType.UPLOADTHING.value in self.folders(self.components.remove):
            core_pairs = self.ut.core_file_pairs()
            remove_files(
                pairs=core_pairs, dirpath=self.paths.lib, ignore_pair_folder=True
            )
