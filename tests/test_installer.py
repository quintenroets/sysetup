from unittest.mock import PropertyMock, patch

import cli
from sysetup.main.installations import install_linter_env
from sysetup.models import Path


def test_linter_env() -> None:
    with Path.tempfile(create=False) as path:
        mocked_path = PropertyMock(return_value=path)
        with patch.object(Path, "linter_env", new_callable=mocked_path):
            install_linter_env()
            python_path = Path.linter_env / "bin" / "python"
            cli.run(f"{python_path} -m pip show autoimport")
