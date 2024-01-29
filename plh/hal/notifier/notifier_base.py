from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import field

from pydantic import dataclasses

from plh.hal.tools import HALDevice

from .contact_info_base import ContactInfoBase
from .conversation_base import ConversationBase, Message
from .response_base import ConversationResponseOptionsEnumBase, ResponseOptionsEnumBase


@dataclasses.dataclass(kw_only=True)
class NotifierBase(HALDevice, ABC):
    """This is a non-blocking notification device."""

    default_contacts: list[ContactInfoBase]
    """Notifications will always be sent to these contacts."""

    conversations: dict[str, ConversationBase] = field(init=False, default_factory=dict)

    @abstractmethod
    def start_conversation(
        self: NotifierBase,
        identifier: str,
        contacts: list[ContactInfoBase],
        response_options: type[ConversationResponseOptionsEnumBase] | None,
    ) -> ConversationBase:
        """Creates a new conversation in the notifier object. If conversation already exists then runtime error is raised."""
        ...

    @abstractmethod
    def end_conversation(self: NotifierBase, identifier: str) -> None:
        """Removes converation from notifier. If conversation does exist then returns."""
        ...

    @abstractmethod
    def send_message(
        self: NotifierBase,
        conversation_identifier: str,
        message: Message,
    ) -> None:
        """Sends message under the specified conversation."""
        ...

    @abstractmethod
    def get_response(
        self: NotifierBase,
        conversation_identifier: str,
    ) -> None | ResponseOptionsEnumBase:
        """Receives response from the specified conversation.
        There are two possible responses: Message and Conversation.
        Response priority: Message > Conversation > None"""
        ...
