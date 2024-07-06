import ast
import asyncio
import aiohttp

import os
from pathlib import Path
import typer

from zentra_models.cli.constants import (
    DEPENDENCY_EXCLUSIONS,
    UI_CORE_FILES,
    GenerateSuccessCodes,
)
from zentra_models.cli.constants.filepaths import GENERATE_PATHS, PACKAGE_PATHS
from zentra_models.cli.local.files import (
    get_file_content,
    get_filename_dir_pairs,
    get_filepaths_list,
)
from zentra_models.cli.local.storage import (
    Dependency,
    NameStorage,
    CountStorage,
    Filepath,
)
from zentra_models.cli.constants.types import LibraryNamePairs


class LocalExtractor:
    """
    Handles the functionality for extracting information from `zentra/models`.

    Parameters:
    - `name_storage` (`storage.BasicNameStorage`) - the Zentra application name storage containing the user model filenames
    """

    def __init__(self, name_storage: BasicNameStorage) -> None:
        self.name_storage = name_storage

        self.model_counts = CountStorage()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name_storage="{self.name_storage}", model_counts="{self.model_counts}")'

    def find_difference(
        self, pair_one: LibraryNamePairs, pair_two: LibraryNamePairs
    ) -> LibraryNamePairs:
        """Identifies the differences between two lists of pairs of Zentra models."""
        same = list(set(pair_one) & set(pair_two))
        return list(set(pair_one + pair_two) - set(same))

    def user_models(self) -> LibraryNamePairs:
        """Retrieves the Zentra model filenames from `zentra/models`."""
        return self.name_storage.filenames

    def existing_models(self) -> LibraryNamePairs:
        """Retrieves the existing Zentra model filenames from the Zentra generate folder."""
        return get_filename_dir_pairs(GENERATE_PATHS.ROOT)

    def model_changes(
        self, existing: LibraryNamePairs, user_models: LibraryNamePairs
    ) -> tuple[LibraryNamePairs, LibraryNamePairs]:
        """Provides two lists of `FolderFilePair` changes. In the form of: `(to_add, to_remove)`."""
        to_remove, to_add = [], []
        existing_models_set = set(existing)

        model_updates = self.find_difference(existing, user_models)
        for model in model_updates:
            if model in existing_models_set:
                to_remove.append(model)
                self.model_counts.remove += 1
            else:
                to_add.append(model)
                self.model_counts.generate += 1

        return to_add, to_remove

    @staticmethod
    def no_new_components_check(
        user_models: LibraryNamePairs, existing: LibraryNamePairs
    ) -> None:
        """Raises an error if there are no new components to create."""
        if user_models == existing:
            raise typer.Exit(code=GenerateSuccessCodes.NO_NEW_COMPONENTS)


class FileExtractor:
    """A helper class for extracting files from a package directory dynamically and converting them to local paths."""

    def __init__(self, root: Path, local: Path, ignore: list[str] = None) -> None:
        self.root = root
        self.local = local
        self.ignore = ignore if ignore else []

    def get_files(self) -> list[Path]:
        """Returns a list of all the paths in the root directory excluding the `ignore` list."""
        paths = []
        for path in self.root.rglob("*"):
            if path.is_file() and not any(
                ignored in path.parts for ignored in self.ignore
            ):
                paths.append(path)
        return paths

    def get_local_paths(self, depth: int = 2) -> list[Path]:
        """Extracts the last values of the root paths based on depth and updates them to the local path."""
        paths = self.get_files()

        new_paths = []
        for file in paths:
            parts = [part.replace("root", "") for part in file.parts[-depth:]]
            new_paths.append(Path(self.local, *parts))

        return new_paths


class ZentraExtractor(ast.NodeVisitor):
    """Extracts the `Zentra` object from the `zentra/models` config file."""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.zentra = None

        self.extract()

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visits the `Assign` nodes in the `ast` tree and stores the `Zentra` object in `self.zentra`"""
        if (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Name)
            and node.value.func.id == "Zentra"
        ):
            self.zentra = node

        self.generic_visit(node)

    def extract(self) -> None:
        """Extracts the `Zentra` object from the filepath and stores it to the `self.zentra` object."""
        file_content = get_file_content(self.filepath)
        tree = ast.parse(file_content, filename=self.filepath)
        self.visit(tree)


class PackageExtractor:
    """A helper class for extracting package dependencies for each component."""

    def __init__(self) -> None:
        self.exclude = DEPENDENCY_EXCLUSIONS

    def get_packages(self, filepath: Path) -> tuple[list[str], list[str]]:
        """A helper function to extract the `(local, external)` dependencies for a package."""
        external_packages = set()
        local_packages = set()

        for package in self.extract_dependencies(filepath):
            if package.startswith("@/"):
                local_packages.add(package)
            else:
                external_packages.add(package)

        return list(local_packages), list(external_packages)

    async def get_versions(self, packages: list[str]) -> list[Dependency]:
        """Retrieves a set of package versions and returns them as a list of `Dependency` models."""
        results = await self.get_package_versions(packages)

        deps = []
        for name, version in results:
            deps.append(Dependency(name=name, version=version))
        return deps

    def extract_dependencies(self, filepath: str, line_depth: int = 15) -> list[str]:
        """Extracts the `from` names from the import statements from a file."""
        with open(filepath, "r") as f:
            content = f.readlines()

        packages = [
            line.split("from")[-1].strip().strip(';"')
            for line in content[:line_depth]
            if "from" in line
        ]

        return [package for package in packages if package not in self.exclude]

    async def fetch_package_version(
        self, session: aiohttp.ClientSession, package_name: str
    ) -> tuple[str, str | None]:
        """Fetch the latest version of an NPM package from the `npm` registry."""
        url = f"https://registry.npmjs.org/{package_name}/latest"
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                package_info = await response.json()
                return package_name, package_info.get("version")
        except aiohttp.ClientError as e:
            print(f"Error fetching package info for {package_name}: {e}")
            return package_name, None

    async def get_package_versions(
        self, package_names: list[str]
    ) -> list[tuple[str, str | None]]:
        """Fetch the latest versions of multiple `NPM` packages concurrently."""
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch_package_version(session, package_name)
                for package_name in package_names
            ]
            return await asyncio.gather(*tasks)
