from __future__ import annotations

from enum import Enum, EnumMeta, StrEnum


class ResponseEnumMeta(EnumMeta):
    def __getitem__(self: ResponseEnumMeta, name: str) -> Enum:
        return {k.lower(): self._member_map_[k] for k in self._member_map_}[
            name.lower()
        ]


class ResponseEnum(StrEnum, metaclass=ResponseEnumMeta):
    ...
