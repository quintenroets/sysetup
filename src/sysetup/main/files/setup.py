from sysetup.main.files import assets, permissions, settings


def setup() -> None:
    permissions.setup()
    assets.setup()
    settings.set_background()
    settings.remove_clutter()
