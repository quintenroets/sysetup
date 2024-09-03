from unittest.mock import MagicMock, patch

from package_dev_utils.tests.args import no_cli_args

from sysetup.main.main import main


@no_cli_args
@patch("sysetup.main.main.setup")
def test_main(mocked_setup: MagicMock) -> None:
    main()
    mocked_setup.assert_called_once()
