from unittest.mock import MagicMock, patch

from package_dev_utils.tests.args import no_cli_args

from sysetup.main.main import main


@no_cli_args
@patch("sysetup.main.files.remove_clutter")
@patch("sysetup.main.main.install_personal_git_repositories")
@patch("sysetup.main.files.configure_ssh")
@patch("sysetup.main.files.configure_git")
def test_main(
    configure_git: MagicMock,
    configure_ssh: MagicMock,
    install_personal_git_repositories: MagicMock,
    remove_clutter: MagicMock,
) -> None:
    main()
    configure_git.assert_called_once()
    configure_ssh.assert_called_once()
    install_personal_git_repositories.assert_called_once()
    remove_clutter.assert_called_once()
