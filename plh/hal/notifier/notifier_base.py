from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import field

from pydantic import dataclasses

from plh.hal.tools import HALDevice

from .contact_info_base import ContactInfoBase
from .conversation_base import ConversationBase, Message
from .response_base import (
    ConversationResponseOptionsEnumBase,
)


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
        opening_text: str,
        contacts: list[ContactInfoBase],
        response_options: type[
            ConversationResponseOptionsEnumBase
        ] = ConversationResponseOptionsEnumBase,
    ) -> None:
        """Creates a new conversation in the notifier object. If conversation already exists then runtime error is raised.
        It would be nice to send a message to contacts informing them the conversation has started.
        """
        ...

    @abstractmethod
    def end_conversation(
        self: NotifierBase,
        identifier: str,
        closing_text: str,
    ) -> None:
        """Removes converation from notifier. If conversation does not exist then returns.
        It would be nice to send a message to contacts informing them the conversation is ended.
        """
        ...

    @abstractmethod
    def send_message(
        self: NotifierBase,
        conversation_identifier: str,
        message: Message,
    ) -> None:
        """Sends message under the specified conversation."""
        ...

    def get_conversation_response(
        self: NotifierBase,
        conversation_identifier: str,
    ) -> None | ConversationResponseOptionsEnumBase:
        """Receives response from the specified conversation if one is available.
        Immediately resets the conversation response upon return."""
        try:
            conversation = self.conversations[conversation_identifier]
        except KeyError:
            raise RuntimeError("Conversation Identifier not recognized.")

        response = conversation.response
        conversation.response = None

        return response
