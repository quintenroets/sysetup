from unittest.mock import MagicMock, patch

from package_dev_utils.tests.args import no_cli_args

from sysetup import cli


@no_cli_args
@patch("sysetup.main.main.setup")
def test_entry_point(mocked_setup: MagicMock) -> None:
    cli.entry_point()
    mocked_setup.assert_called_once()
