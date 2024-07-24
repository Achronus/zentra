from pathlib import Path
import pytest
import requests
import responses
import toml

from zentra_api.cli.builder.poetry import (
    Description,
    Script,
    PipPackage,
    PoetryFile,
    PoetryFileBuilder,
)
from zentra_api.cli.constants import PYTHON_VERSION, pypi_url


def test_description():
    desc = Description(name="test_project")

    target = {
        "name": "test_project",
        "version": "0.1.0",
        "description": "A FastAPI backend for processing API data.",
        "authors": ["Placeholder <placeholder@email.com>"],
        "readme": "README.md",
    }
    assert desc.model_dump() == target


def test_script():
    script = Script(name="run-dev", command="app.run:development")
    target = {"name": "run-dev", "command": "app.run:development"}
    assert script.model_dump() == target


class TestPipPackage:
    @staticmethod
    def test_no_trim_version():
        package = PipPackage(name="pytest", version="2")
        target = {
            "name": "pytest",
            "version": "^2",
        }
        assert package.model_dump() == target

    @staticmethod
    def test_trim_version():
        package = PipPackage(name="python", version=PYTHON_VERSION)
        target = {
            "name": "python",
            "version": "^3.12",
        }
        assert package.model_dump() == target


def test_poetry_file():
    core_deps = [PipPackage(name="fastapi", version="0.111.1")]
    dev_deps = [PipPackage(name="pytest", version="2.0.0")]
    description = Description(name="test_project")
    scripts = [
        Script(name="run-dev", command="app.run:development"),
        Script(name="run-prod", command="app.run:production"),
    ]

    poetry_file = PoetryFile(
        desc=description,
        scripts=scripts,
        core_deps=core_deps,
        dev_deps=dev_deps,
    )

    target = {
        "tool": {
            "poetry": {
                "name": "test_project",
                "version": "0.1.0",
                "description": "A FastAPI backend for processing API data.",
                "authors": ["Placeholder <placeholder@email.com>"],
                "readme": "README.md",
            },
            "scripts": {
                "run-dev": "app.run:development",
                "run-prod": "app.run:production",
            },
            "dependencies": {
                "python": "^3.12",
                "fastapi": "^0.111",
            },
            "group": {
                "dev": {
                    "dependencies": {
                        "pytest": "^2.0",
                    },
                }
            },
        },
        "build-system": {
            "requires": ["poetry-core"],
            "build-backend": "poetry.core.masonry.api",
        },
    }

    assert poetry_file.to_dict() == target


class TestPoetryFileBuilder:
    @pytest.fixture
    def builder(self) -> PoetryFileBuilder:
        return PoetryFileBuilder(project_name="test_project", test_logging=True)

    @pytest.fixture
    def target_file(self) -> PoetryFile:
        return PoetryFile(
            desc=Description(name="test_project"),
            scripts=[
                Script(name="run-dev", command="app.run:development"),
                Script(name="run-prod", command="app.run:production"),
            ],
            core_deps=[PipPackage(name="flask", version="1.2.3")],
            dev_deps=[PipPackage(name="pytest", version="2.3.4")],
        )

    @pytest.fixture
    def target_json(self) -> dict:
        return {
            "tool": {
                "poetry": {
                    "name": "test_project",
                    "version": "0.1.0",
                    "description": "A FastAPI backend for processing API data.",
                    "authors": ["Placeholder <placeholder@email.com>"],
                    "readme": "README.md",
                },
                "scripts": {
                    "run-dev": "app.run:development",
                    "run-prod": "app.run:production",
                },
                "dependencies": {
                    "python": "^3.12",
                    "flask": "^1.2",
                },
                "group": {
                    "dev": {
                        "dependencies": {
                            "pytest": "^2.3",
                        },
                    }
                },
            },
            "build-system": {
                "requires": ["poetry-core"],
                "build-backend": "poetry.core.masonry.api",
            },
        }

    @responses.activate
    def test_build(self, builder: PoetryFileBuilder, target_file: PoetryFile):
        core_package = "flask"
        dev_package = "pytest"

        responses.add(
            responses.GET,
            pypi_url(core_package),
            json={"info": {"version": "1.2.3"}},
            status=200,
        )

        responses.add(
            responses.GET,
            pypi_url(dev_package),
            json={"info": {"version": "2.3.4"}},
            status=200,
        )

        result = builder.build([core_package], [dev_package])
        assert result == target_file

    @responses.activate
    def test_update(
        self, tmp_path: Path, builder: PoetryFileBuilder, target_json: dict
    ):
        core_package = "flask"
        dev_package = "pytest"

        responses.add(
            responses.GET,
            pypi_url(core_package),
            json={"info": {"version": "1.2.3"}},
            status=200,
        )

        responses.add(
            responses.GET,
            pypi_url(dev_package),
            json={"info": {"version": "2.3.4"}},
            status=200,
        )

        filepath = Path(tmp_path, "test.toml")
        builder.update(filepath, [core_package], [dev_package])

        with open(filepath, "r") as f:
            result = toml.load(f)

        assert result == target_json

    class TestGetPackages:
        @responses.activate
        def test_success(self, builder: PoetryFileBuilder):
            package1 = "flask"
            package2 = "pytest"

            responses.add(
                responses.GET,
                pypi_url(package1),
                json={"info": {"version": "1.2.3"}},
                status=200,
            )

            responses.add(
                responses.GET,
                pypi_url(package2),
                json={"info": {"version": "2.3.4"}},
                status=200,
            )

            result = builder.get_packages([package1, package2])

            checks = [
                len(result) == 2,
                result[0].name == "flask",
                result[0].version == "^1.2",
                result[1].name == "pytest",
                result[1].version == "^2.3",
            ]
            assert all(checks)

        @responses.activate
        def test_get_packages_http_error(self, builder: PoetryFileBuilder):
            package = "nonexistent-package"
            responses.add(responses.GET, pypi_url(package), status=404)

            result = builder.get_packages([package])
            assert len(result) == 0

        @responses.activate
        def test_get_packages_request_exception(self, builder: PoetryFileBuilder):
            # Mock a request exception
            package = "example-package"
            responses.add(
                responses.GET,
                pypi_url(package),
                body=requests.RequestException("Connection error"),
            )

            result = builder.get_packages([package])
            assert len(result) == 0
