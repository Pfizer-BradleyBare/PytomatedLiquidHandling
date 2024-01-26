from __future__ import annotations

import contextlib

from pydantic import dataclasses as _dataclasses


@_dataclasses.dataclass(kw_only=True)
class ContactInfo:
    """Info required to notify a user."""

    name: str
    """Name of the user to notify."""

    emails: list[str]
    """Email to send notification."""

    phone_numbers: list[str]
    """Phone number to send notification."""


_contacts: dict[str, ContactInfo] = {}


def add_contact(contact: ContactInfo) -> None:
    _contacts[contact.name] = contact


def delete_contact(contact: ContactInfo) -> None:
    with contextlib.suppress(KeyError):
        del _contacts[contact.name]


def delete_all_contacts() -> None:
    global _contacts
    _contacts = {}
