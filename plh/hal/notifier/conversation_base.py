from __future__ import annotations

import dataclasses

from .contact_info_base import ContactInfoBase
from .response_base import (
    ConversationResponseOptionsEnumBase,
    MessageResponseOptionsEnumBase,
)


@dataclasses.dataclass(kw_only=True)
class Message:
    """A message that may or may not require a response"""

    subject: str
    """The reason for the message."""

    extra_text: str | None
    """Additional information relating to the subject."""

    response_options: type[MessageResponseOptionsEnumBase] = MessageResponseOptionsEnumBase
    """If the message requires a response, what are the optons?"""

    response: None | MessageResponseOptionsEnumBase = dataclasses.field(
        init=False,
        default=None,
    )
    """The response received."""

    def get_body(self: Message, conversation_response_options: type[ConversationResponseOptionsEnumBase]) -> str:
        newline = "\n"
        body = f"{self.subject}\n\n"

        if self.extra_text is not None:
            body += f"{self.extra_text}\n\n"

        if len(self.response_options) > 0:
            body += "You may send the following responses to this message only:\n"
            body += f"{newline.join([f'"{i.name}" for {i.value}' for i in self.response_options])}\n\n"

        if len(conversation_response_options) > 0:
            body += "You may send the following responses at any time to get more information:\n"
            body += f"{newline.join([f'"{i.name}" for {i.value}' for i in conversation_response_options])}\n\n"

        body += "\n"
        body += "Thanks!"
        return body

@dataclasses.dataclass(kw_only=True)
class ConversationBase:
    """A collection of communications categorized by a subject"""

    identifier: str
    """This will be used to group messages. Must be guarenteed unique."""
    """It's best to have the following format: '<date> <high level subject> <system info> <system serial number>'."""

    contacts: list[ContactInfoBase]
    """Contact who receive messages."""

    messages: list[Message] = dataclasses.field(init=False, default_factory=list)
    """All communications that occured. By default the last communication may be the one that needs a response."""

    response_options: type[ConversationResponseOptionsEnumBase]
    """These are options that can be sent at anytime. These are only valid conversation responses."""

    response: None | ConversationResponseOptionsEnumBase = dataclasses.field(
        init=False,
        default=None,
    )

t = ConversationBase(identifier="",contacts=[],response_options=ConversationResponseOptionsEnumBase)

t.response = t.response_options["a"]
