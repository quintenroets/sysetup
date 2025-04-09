from typing import TypeVar, cast

import superpathlib
from simple_classproperty import classproperty
from typing_extensions import Self

T = TypeVar("T", bound="Path")


class Path(superpathlib.Path):
    @classmethod
    @classproperty
    def source_root(cls) -> Self:
        return cls(__file__).parent.parent

    @classmethod
    @classproperty
    def assets(cls) -> Self:
        path = cls.script_assets / cls.source_root.name
        return cast("Self", path)

    @classmethod
    @classproperty
    def config(cls) -> Self:
        path = cls.assets / "config" / "config.yaml"
        return cast("Self", path)

    @classmethod
    @classproperty
    def packages(cls: type[T]) -> T:
        path = cls.assets / "packages"
        return cast(T, path)

    @classmethod
    @classproperty
    def extensions(cls: type[T]) -> T:
        path = cls.HOME / ".local" / "share" / "extensions"
        return cast(T, path)

    @classmethod
    @classproperty
    def update_wallpaper_script(cls: type[T]) -> T:
        path = cls.source_root / "assets" / "scripts" / "update_wallpaper.js"
        return cast(T, path)
