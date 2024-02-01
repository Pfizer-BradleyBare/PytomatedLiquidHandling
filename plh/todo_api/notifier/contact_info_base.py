from __future__ import annotations

from pydantic import dataclasses as _dataclasses


@_dataclasses.dataclass(kw_only=True)
class ContactInfoBase:
    """Info required to notify a user."""

    name: str
    """Name of the user to notify."""
