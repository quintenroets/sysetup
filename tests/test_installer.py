from sysetup.installer import get_vnc_download_url


def test_vnc_url():
    url = get_vnc_download_url()
    assert "VNC" in url
