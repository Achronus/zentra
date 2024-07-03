import ast
import typer

import aiohttp
import asyncio

from zentra_models.cli.conf.checks import (
    CheckConfigFileValid,
    check_file_exists,
    check_folder_exists,
    check_zentra_exists,
)

from zentra_models.cli.constants import (
    DEPENDENCY_EXCLUSIONS,
    CommonErrorCodes,
    GenerateSuccessCodes,
)
from zentra_models.cli.constants.filepaths import LOCAL_PATHS
from zentra_models.cli.local.files import (
    get_file_content,
    get_file_content_lines,
)
from zentra_models.cli.local.storage import Dependency, DependencyStorage
from zentra_models.cli.commands.generate.generate import GenerateController
from zentra_models.cli.display.printables import generate_complete_panel

from rich.console import Console

console = Console()


class Generate:
    """A class for handling the logic for the `zentra generate` command."""

    def __init__(self) -> None:
        self.local_paths = LOCAL_PATHS
        self.config = self.local_paths.CONF

    def init_checks(self) -> None:
        """Performs various checks to immediately provide feedback to the user regarding missing files."""
        if not check_folder_exists(self.local_paths.MODELS):
            raise typer.Exit(code=CommonErrorCodes.MODELS_DIR_MISSING)

        if not check_file_exists(self.config):
            raise typer.Exit(code=CommonErrorCodes.CONFIG_MISSING)

        if len(get_file_content_lines(self.config)) == 0:
            raise typer.Exit(code=CommonErrorCodes.CONFIG_EMPTY)

    def check_config_valid(self) -> None:
        """Checks if the config file is valid. Raises an error if False."""
        check_config = CheckConfigFileValid()
        file_content_tree = ast.parse(get_file_content(self.config))
        check_config.visit(file_content_tree)

        valid_content = check_config.is_valid()

        if not valid_content:
            raise typer.Exit(code=CommonErrorCodes.INVALID_CONFIG)

    def create_components(self) -> None:
        """Generates the react components based on the `zentra/models` folder."""
        self.check_config_valid()
        zentra = check_zentra_exists(self.local_paths.MODELS)

        if not zentra:
            raise typer.Exit(CommonErrorCodes.MODELS_DIR_MISSING)

        if len(zentra.name_storage.components) == 0:
            raise typer.Exit(code=CommonErrorCodes.NO_COMPONENTS)

        console.print()
        controller = GenerateController(zentra)
        controller.run()

        console.print(generate_complete_panel(controller.storage))
        raise typer.Exit(GenerateSuccessCodes.COMPLETE)


class DependencyManager:
    """A helper class for handling the `package.json` dependencies for each library."""

    def __init__(self, filepaths: list[str]) -> None:
        self.filepaths = filepaths
        self.exclude = DEPENDENCY_EXCLUSIONS

        self.storage = DependencyStorage()

    async def extraction(self) -> None:
        """Extracts information from the list of `self.filepaths` and stores them in a container."""
        external_packages = set()
        local_packages = set()
        for file in self.filepaths:
            for package in self.extract_dependencies(file):
                if package.startswith("@/"):
                    local_packages.add(package)
                else:
                    external_packages.add(package)

        self.storage.local = list(local_packages)

        results = await self.get_package_versions(list(external_packages))

        for name, version in results:
            self.storage.external.append(Dependency(name=name, version=version))

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
