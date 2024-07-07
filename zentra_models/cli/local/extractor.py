import ast
import asyncio
import aiohttp

from pathlib import Path

from zentra_models.cli.constants import DEPENDENCY_EXCLUSIONS

from zentra_models.cli.local.files import get_file_content
from zentra_models.cli.local.storage import Dependency


class LocalFileExtractor:
    """A helper class for extracting files from a local directory."""

    def __init__(self, root: Path, ignore: list[str] = None) -> None:
        self.root = root
        self.ignore = ignore if ignore else []

    def get_paths(self) -> list[Path]:
        """Returns a list of paths in a directory excluding the `ignore` list."""
        paths = []
        for path in self.root.rglob("*"):
            if path.is_file() and not any(
                ignored in path.parts for ignored in self.ignore
            ):
                paths.append(path)
        return paths


class PackageFileExtractor:
    """A helper class for extracting files from a package directory dynamically and converting them to local paths."""

    def __init__(self, root: Path, local: Path) -> None:
        self.root = root
        self.local = local

    def __get_paths(self, dirpath: Path, ignore: list[str]) -> list[Path]:
        """Returns a list of paths in a directory excluding the `ignore` list."""
        paths = []
        for path in dirpath.rglob("*"):
            if path.is_file() and not any(ignored in path.parts for ignored in ignore):
                paths.append(path)
        return paths

    def get_root_paths(self, ignore: list[str] = []) -> list[Path]:
        """Returns a list of all the paths in the local directory."""
        return self.__get_paths(self.root, ignore)

    def get_local_paths(self) -> list[Path]:
        """Returns a list of all the paths in the root directory."""
        return self.__get_paths(self.local, ignore=[])

    def create_local_paths(self, ignore: list[str], depth: int = 2) -> list[Path]:
        """Extracts the last values of the root paths based on depth and updates them to the local path."""
        paths = self.__get_paths(self.root, ignore)

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
