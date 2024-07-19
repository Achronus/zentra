import os
from pathlib import Path
import pytest

from zentra_models.cli.local.storage import (
    AppStorage,
    ComponentDetails,
    ComponentStorage,
    ConfigExistStorage,
    Dependency,
    Filepath,
    NameStorage,
)


@pytest.fixture
def comp_details() -> ComponentDetails:
    return ComponentDetails(
        name="Button",
        library="ui",
        path=Filepath(
            filename="button.tsx",
            local=Path(os.getcwd(), "ui", "button.tsx"),
            package=Path(os.getcwd(), "other", "button.tsx"),
        ),
        children=[
            Filepath(
                filename="child.tsx",
                local=Path(os.getcwd(), "ui", "child.tsx"),
                package=Path(os.getcwd(), "other", "child.tsx"),
            )
        ],
    )


@pytest.fixture
def comp_storage(comp_details) -> ComponentStorage:
    return ComponentStorage(items=[comp_details])


class TestConfigExistStorage:
    @pytest.fixture
    def storage(self) -> ConfigExistStorage:
        return ConfigExistStorage()

    @staticmethod
    def test_app_configured_false(storage: ConfigExistStorage):
        assert not storage.app_configured()

    @staticmethod
    def test_app_configured_valid(storage: ConfigExistStorage):
        storage.models_folder_exists = True
        storage.config_file_exists = True
        storage.root_exists = True
        assert storage.app_configured()


class TestComponentDetails:
    @staticmethod
    def test_local_paths(comp_details: ComponentDetails):
        result = comp_details.local_paths()
        target = [
            Path(os.getcwd(), "ui", "button.tsx"),
            Path(os.getcwd(), "ui", "child.tsx"),
        ]
        result.sort()
        target.sort()
        assert result == target

    @staticmethod
    def test_package_paths(comp_details: ComponentDetails):
        result = comp_details.package_paths()
        target = [
            Path(os.getcwd(), "other", "button.tsx"),
            Path(os.getcwd(), "other", "child.tsx"),
        ]
        result.sort()
        target.sort()
        assert result == target


class TestComponentStorage:
    @staticmethod
    def test_local_paths(comp_storage: ComponentStorage):
        result = comp_storage.local_paths()
        target = [
            Path(os.getcwd(), "ui", "button.tsx"),
            Path(os.getcwd(), "ui", "child.tsx"),
        ]
        result.sort()
        target.sort()
        assert result == target

    @staticmethod
    def test_package_paths(comp_storage: ComponentStorage):
        result = comp_storage.package_paths()
        target = [
            Path(os.getcwd(), "other", "button.tsx"),
            Path(os.getcwd(), "other", "child.tsx"),
        ]
        result.sort()
        target.sort()
        assert result == target


class TestAppStorage:
    @pytest.fixture
    def name_storage(self) -> NameStorage:
        return NameStorage(
            files=["AgencyDetails", "Homepage", "Navbar"],
            blocks=["AgencyForm", "Homepage", "Navbar"],
            components=["Button", "Avatar", "AlertDialog"],
            libraries=["ui", "uploadthing"],
        )

    @pytest.fixture
    def packages(self) -> list[Dependency]:
        return [
            Dependency(name="lucide-react", version="0.400.0"),
            Dependency(name="cmdk", version="1.0.0"),
        ]

    @pytest.fixture
    def app_storage(
        self,
        name_storage: NameStorage,
        comp_storage: ComponentStorage,
        packages: list[Dependency],
    ) -> AppStorage:
        return AppStorage(
            names=name_storage,
            components=comp_storage,
            packages=packages,
        )

    @staticmethod
    def test_add_names(app_storage: AppStorage):
        app_storage.add_names("blocks", ["AgencyDetails"])

        result = app_storage.names.blocks
        target = ["AgencyForm", "Homepage", "Navbar", "AgencyDetails"]
        assert result == target

    @staticmethod
    def test_add_component(comp_details: ComponentDetails, app_storage: AppStorage):
        dummy_comp = ComponentDetails(
            name="test",
            library="ui",
            path=Filepath(
                filename="test.tsx",
                local=Path(os.getcwd()),
                package=Path(os.getcwd()),
            ),
            children=[],
        )

        print(app_storage.components)
        app_storage.add_component(dummy_comp)

        target = ComponentStorage(items=[comp_details, dummy_comp])
        result = app_storage.components.items
        assert target.items == result

    @staticmethod
    def test_add_component_duplicates(
        comp_details: ComponentDetails, app_storage: AppStorage
    ):
        result = app_storage.components.items
        app_storage.add_component(comp_details)
        target = app_storage.components.items
        assert result == target

    @staticmethod
    def test_add_packages(app_storage: AppStorage):
        dummy_dep = Dependency(name="test", version="1.0.0")

        target = app_storage.packages + [dummy_dep]
        app_storage.add_packages([dummy_dep])
        assert app_storage.packages == target

    @staticmethod
    def test_package_dict(app_storage: AppStorage):
        result = app_storage.dependency_dict()

        target = {
            "dependencies": {
                "lucide-react": "0.400.0",
                "cmdk": "1.0.0",
            },
        }

        assert target == result

    @staticmethod
    def test_get_target_components(
        comp_details: ComponentDetails, app_storage: AppStorage
    ):
        result = app_storage.get_target_components()
        target = ComponentStorage(items=[comp_details])

        assert result == target

    @staticmethod
    def test_get_components(comp_details: ComponentDetails, app_storage: AppStorage):
        result = app_storage.get_components(names=["Button"])
        target = ComponentStorage(items=[comp_details])

        assert result == target

    @staticmethod
    def test_get_names(app_storage: AppStorage):
        result = app_storage.get_names()
        target = (
            ["AgencyDetails", "Homepage", "Navbar"],
            ["AgencyForm", "Homepage", "Navbar"],
            ["Button", "Avatar", "AlertDialog"],
        )
        assert result == target

    @staticmethod
    def test_get_name_option(app_storage: AppStorage):
        result = app_storage.get_name_option("libraries")
        target = ["ui", "uploadthing"]
        assert result == target

    @staticmethod
    def test_get_name_option_fail(app_storage: AppStorage):
        with pytest.raises(AttributeError):
            app_storage.get_name_option("test")

    @staticmethod
    def test_count(app_storage: AppStorage):
        result = app_storage.count("libraries")
        assert result == 2
