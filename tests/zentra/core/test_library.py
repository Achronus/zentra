from zentra_models.core.enums.ui import LibraryType
from zentra_models.custom import CustomModel
from zentra_models.nextjs import NextJs
from zentra_models.ui import ShadcnUi
from zentra_models.uploadthing import Uploadthing


class TestNextJs:
    @staticmethod
    def test_library():
        assert NextJs().library == LibraryType.NEXTJS.value


class TestShadcnUi:
    @staticmethod
    def test_library():
        assert ShadcnUi().library == LibraryType.SHADCNUI.value


class TestUploadthing:
    @staticmethod
    def test_library():
        assert Uploadthing().library == LibraryType.UPLOADTHING.value


class TestCustomModel:
    @staticmethod
    def test_library():
        assert CustomModel().library == LibraryType.CUSTOM.value
