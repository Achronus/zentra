import aiohttp
import asyncio

from zentra_models.cli.constants import DEPENDENCY_EXCLUSIONS
from zentra_models.cli.local.storage import Dependency, DependencyStorage


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
