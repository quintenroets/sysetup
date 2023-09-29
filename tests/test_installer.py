import cli

from sysetup.installer import get_vnc_download_url, install_linter_env
from sysetup.path import Path


def test_vnc_url():
    url = get_vnc_download_url()
    assert "VNC" in url


def test_linter_env():
    linter_env_path = Path.HOME / ".local" / "share" / "envs" / "linterenv"
    linter_env_path.rmtree()
    install_linter_env()
    python_path = linter_env_path / "bin" / "python"
    cli.run(f"{python_path} -m pip show autoimport")
