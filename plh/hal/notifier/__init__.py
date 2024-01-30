from __future__ import annotations

from .contact_info_base import ContactInfoBase
from .conversation_base import Message
from .email_notifier import EmailContact, EmailNotifier
from .notifier_base import NotifierBase
from .response_base import (
    ConversationResponseOptionsEnumBase,
    MessageResponseOptionsEnumBase,
)
from .text_notifier import TextContact, TextNotifier

__all__ = [
    "NotifierBase",
    "ContactInfoBase",
    "MessageResponseOptionsEnumBase",
    "ConversationResponseOptionsEnumBase",
    "Message",
    "EmailNotifier",
    "EmailContact",
    "TextContact",
    "TextNotifier",
]

identifier = str
devices: dict[identifier, NotifierBase] = {}

_current_conversation_indentifier: str = "NONE"


def select_conversation(conversation_identifier: str) -> None:
    global _current_conversation_indentifier  # noqa:PLW0603
    _current_conversation_indentifier = conversation_identifier


def start_conversation(
    opening_text: str,
    contacts: list[ContactInfoBase],
    response_options: type[
        ConversationResponseOptionsEnumBase
    ] = ConversationResponseOptionsEnumBase,
) -> None:
    for device in devices.values():
        device._start_conversation(  # noqa:SLF001
            _current_conversation_indentifier,
            opening_text,
            contacts,
            response_options,
        )


def end_conversation(
    closing_text: str,
) -> None:
    for device in devices.values():
        device._end_conversation(  # noqa:SLF001
            _current_conversation_indentifier,
            closing_text,
        )


def send_message(
    message: Message,
) -> None:
    for device in devices.values():
        device._send_message(_current_conversation_indentifier, message)  # noqa:SLF001


def get_conversation_response() -> None | ConversationResponseOptionsEnumBase:
    for device in devices.values():
        response = device._get_conversation_response(  # noqa:SLF001
            _current_conversation_indentifier,
        )

        if response is not None:
            return response

    return None
