from zentra.core.enums.ui import LibraryType
from zentra.custom import CustomModel
from zentra.nextjs import NextJs
from zentra.ui import ShadcnUi
from zentra.uploadthing import Uploadthing


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
