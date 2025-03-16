from typing import TypeVar, cast

import superpathlib
from simple_classproperty import classproperty

T = TypeVar("T", bound="Path")


class Path(superpathlib.Path):
    @classmethod
    @classproperty
    def source_root(cls: type[T]) -> T:
        return cls(__file__).parent.parent

    @classmethod
    @classproperty
    def assets(cls: type[T]) -> T:
        path = cls.script_assets / cls.source_root.name
        return cast(T, path)

    @classmethod
    @classproperty
    def config(cls: type[T]) -> T:
        path = cls.assets / "config" / "config.yaml"
        return cast(T, path)

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

    @classmethod
    @classproperty
    def profile(cls: type[T]) -> T:
        path = cls.HOME / ".bash_profile"
        return cast(T, path)
