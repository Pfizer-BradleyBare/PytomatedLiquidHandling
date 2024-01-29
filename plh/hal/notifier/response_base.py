from __future__ import annotations

from enum import Enum, EnumMeta, FlagBoundary, StrEnum, _EnumDict
from typing import Any


class ResponseOptionsEnumMeta(EnumMeta):
    """Custom enum metaclass to enable the following:
    1. Case-insensitive indexing.
    2. Subclassing with Enum members defined in parent classes.
    3. Parent enum members also available in subclass _member_map_.

    NOTE: Type checking will complain that Enums with members cannot be subclassed. You may ignore that warning.
    """

    def __getitem__(self: ResponseOptionsEnumMeta, name: str) -> Enum:
        """Case insensitive indexing."""
        return {k.lower(): self._member_map_[k] for k in self._member_map_}[
            name.lower()
        ]

    @classmethod
    def _check_for_existing_members_(mcls, class_name, bases):
        """Eliminates subclassing restriction."""
        ...

    def __new__(
        metacls: type[ResponseOptionsEnumMeta],
        cls: str,
        bases: tuple[type, ...],
        classdict: _EnumDict,
        *,
        boundary: FlagBoundary | None = None,
        _simple: bool = False,
        **kwds: Any,
    ) -> ResponseOptionsEnumMeta:
        """Copies parent member info into subclass."""

        enum = super().__new__(
            metacls,
            cls,
            bases,
            classdict,
            boundary=boundary,
            _simple=_simple,
            **kwds,
        )

        if any(name in enum.__mro__[1]._member_names_ for name in enum._member_names_):  # type: ignore
            raise TypeError("Enum members must be unique through inheritance.")
        # ensure all member names are unique.

        enum._member_map_.update(enum.__mro__[1]._member_map_)  # type: ignore
        enum._member_names_ += enum.__mro__[1]._member_names_  # type: ignore
        enum._value2member_map_.update(enum.__mro__[1]._value2member_map_)  # type: ignore
        # Update subclass member info with the member info from the parent.

        return enum


class ResponseOptionsEnumBase(StrEnum, metaclass=ResponseOptionsEnumMeta):
    """Base class for all possible responses for a notification.
    Response options should be a subclass of this with their own custom options."""


class MessageResponseOptionsEnumBase(ResponseOptionsEnumBase):
    ...


class ConversationResponseOptionsEnumBase(ResponseOptionsEnumBase):
    ...
