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
    "set_conversation",
    "start_conversation",
    "end_conversation",
    "send_message",
    "get_conversation_response",
    "NotifierBase",
    "ContactInfoBase",
    "Message",
    "MessageResponseOptionsEnumBase",
    "ConversationResponseOptionsEnumBase",
    "EmailNotifier",
    "EmailContact",
    "TextNotifier",
    "TextContact",
]

identifier = str
devices: dict[identifier, NotifierBase] = {}

_current_conversation_indentifier: str = "NONE"


def set_conversation(conversation_identifier: str) -> None:
    """Sets the conversation for ```start_conversation```, ```end_conversation```, ```send_message```, and ```get_conversation_response```.
    You should always set the conversation before calling any functions.
    """
    global _current_conversation_indentifier  # noqa:PLW0603
    _current_conversation_indentifier = conversation_identifier


def start_conversation(
    opening_text: str,
    contacts: list[ContactInfoBase],
    response_options: type[
        ConversationResponseOptionsEnumBase
    ] = ConversationResponseOptionsEnumBase,
) -> None:
    """Starts a conversation defined by ```set_conversation``` across all notifier devices."""
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
    """Ends a conversation defined by ```set_conversation``` across all notifier devices."""
    for device in devices.values():
        device._end_conversation(  # noqa:SLF001
            _current_conversation_indentifier,
            closing_text,
        )


def send_message(
    message: Message,
) -> None:
    """Sends a message through the conversation defined by ```set_conversation``` across all notifier devices."""
    for device in devices.values():
        device._send_message(_current_conversation_indentifier, message)  # noqa:SLF001


def get_conversation_response() -> None | ConversationResponseOptionsEnumBase:
    """Returns the high level conversation response in the conversation defined by ```set_conversation```."""
    for device in devices.values():
        response = device._get_conversation_response(  # noqa:SLF001
            _current_conversation_indentifier,
        )

        if response is not None:
            return response

    return None
