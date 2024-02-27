import typing
from typing import TypeVar

import superpathlib
from simple_classproperty import classproperty

T = TypeVar("T", bound="Path")


class Path(superpathlib.Path):
    @classmethod
    @classproperty
    def source_root(cls: type[T]) -> T:
        return cls(__file__).parent

    @classmethod
    @classproperty
    def assets(cls: type[T]) -> T:
        path = cls.script_assets / cls.source_root.name
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def config(cls: type[T]) -> T:
        path = cls.assets / "config" / "config.yaml"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def packages(cls: type[T]) -> T:
        path = cls.assets / "packages"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def linter_env(cls: type[T]) -> T:
        path = cls.assets / "linterenv"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def extensions(cls: type[T]) -> T:
        path = cls.HOME / ".local" / "share" / "extensions"
        return typing.cast(T, path)

    @classmethod
    @classproperty
    def update_wallpaper_script(cls: type[T]) -> T:
        path = cls.source_root / "assets" / "scripts" / "update_wallpaper.js"
        return typing.cast(T, path)
