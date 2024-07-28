import pytest
from pydantic import ValidationError
from zentra_api.validation import EnvFilename


class TestEnvFilename:
    @staticmethod
    def test_valid_filename():
        valid_filenames = [
            ".env",
            ".env.local",
            ".env.production",
            ".env.test",
            ".env.custom-1",
        ]

        for filename in valid_filenames:
            env_filename = EnvFilename(name=filename)
            assert env_filename.name == filename

    @staticmethod
    def test_invalid_filename():
        invalid_filenames = [
            "env",
            ".env.",
            ".env..local",
            ".env/production",
            ".env@custom",
        ]

        for filename in invalid_filenames:
            with pytest.raises(ValidationError):
                EnvFilename(name=filename)
