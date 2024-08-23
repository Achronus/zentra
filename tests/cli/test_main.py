from unittest.mock import patch
import pytest

import typer
from typer.testing import CliRunner

from zentra_sdk.cli.commands.setup import Setup
from zentra_sdk.cli.main import app

runner = CliRunner()


class TestInit:
    @staticmethod
    def test_success():
        with patch.object(Setup, "build", return_value=None) as mock_build:
            result = runner.invoke(app, ["init"])

            assert result.exit_code == 0
            mock_build.assert_called_once()

    @staticmethod
    def test_extra_args():
        result = runner.invoke(app, ["init", "test"])
        assert result.exit_code != 0

    @staticmethod
    def test_typer_error():
        with patch.object(Setup, "build", side_effect=typer.Exit(code=-1)):
            result = runner.invoke(app, ["init"])

            assert result.exit_code == 0
