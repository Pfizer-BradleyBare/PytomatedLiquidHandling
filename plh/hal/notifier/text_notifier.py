from __future__ import annotations

from dataclasses import field

from pydantic import dataclasses
from redmail.email.sender import EmailSender

from .contact_info_base import *
from .contact_info_base import ContactInfoBase
from .conversation_base import ConversationBase, Message
from .notifier_base import *
from .notifier_base import NotifierBase
from .response_base import *
from .response_base import (
    ConversationResponseOptionsEnumBase,
    MessageResponseOptionsEnumBase,
)

carrier_domains = {
    "AT&T": "mms.att.net",
    "T-Mobile": "tmomail.net",
    "Verizon": "vzwpix.com",
    "Sprint": "pm.sprint.com",
    "Virgin Mobile": "vmpix.com",
    "Metro PCS": "mymetropcs.com",
    "Boost Mobile": "myboostmobile.com",
    "Cricket": "mms.cricketwireless.net",
    "Google Fi": "msg.fi.google.com",
    "U.S. Cellular": "email.uscc.net",
    "Consumer Cellular": "mailmymobile.net",
}
# NOT USED BUT KEPT JUST INCASE


@dataclasses.dataclass(kw_only=True)
class TextContact(ContactInfoBase):
    phone_number: str

    def __post_init__(self: TextContact) -> None:
        self.phone_number = self.phone_number.replace("-", "")


@dataclasses.dataclass(kw_only=True)
class TextConversation(ConversationBase):
    contacts: list[TextContact]

    def get_phone_numbers(self: TextConversation) -> list[str]:
        return [
            f"{contact.phone_number}@{carrier_domain}"
            for contact in self.contacts
            for carrier_domain in carrier_domains.values()
        ]


@dataclasses.dataclass(kw_only=True)
class TextNotifier(NotifierBase):
    smtp_host: str
    smtp_port: int
    sender_email: str

    default_contacts: list[TextContact]

    conversations: dict[str, TextConversation] = field(
        init=False,
        default_factory=dict,
    )

    def _get_body(
        self: TextNotifier,
        conversation: TextConversation,
        message: Message,
    ) -> str:
        body = f"{message.subject}\n\n"

        if message.extra_text is not None:
            body += f"{message.extra_text}\n\n"

        newline = "\n"

        if len(message.response_options) > 0:
            body += "You may send the following responses to this message only:\n"
            body += newline.join(
                [f'"{i.name}" for {i.value.lower()}' for i in message.response_options],
            )
            body += "\n\n"

        if len(conversation.response_options) > 0:
            body += "You may send the following responses at any time:\n"
            body += newline.join(
                [
                    f'"{i.name}" for {i.value.lower()}'
                    for i in conversation.response_options
                ],
            )
            body += "\n\n"

        body += "NOTE: You cannot respond directly to this text. Instead, you must send an email or text to the following with your response:\n"
        body += f"Email: {self.sender_email}\n"
        body += f"Subject: {conversation.identifier}\n"

        body += "\n"
        body += "Thanks!"
        return body

    def start_conversation(
        self: TextNotifier,
        conversation_identifier: str,
        opening_text: str,
        contacts: list[ContactInfoBase],
        response_options: type[
            ConversationResponseOptionsEnumBase
        ] = ConversationResponseOptionsEnumBase,
    ) -> None:
        if conversation_identifier in self.conversations:
            raise RuntimeError("Conversation already exists.")

        sender = EmailSender(host=self.smtp_host, port=self.smtp_port)

        message = Message(
            subject=opening_text,
            extra_text=None,
            response_options=MessageResponseOptionsEnumBase,
        )
        # Our message subject will be an initial line.
        # Extra text is a following remark with more info.

        conversation = TextConversation(
            identifier=conversation_identifier,
            contacts=[
                contact for contact in contacts if isinstance(contact, TextContact)
            ]
            + self.default_contacts,
            response_options=response_options,
        )

        self.conversations[conversation_identifier.replace(" ", "")] = conversation
        # create the conversation

        conversation.messages.append(message)

        sender.send(
            subject=conversation.identifier,
            sender=self.sender_email,
            receivers=conversation.get_phone_numbers(),
            text=self._get_body(conversation, message),
        )

    def end_conversation(
        self: TextNotifier,
        conversation_identifier: str,
        closing_text: str,
    ) -> None:
        conversation_identifier = conversation_identifier.replace(" ", "")

        if conversation_identifier not in self.conversations:
            return

        conversation = self.conversations[conversation_identifier]

        del self.conversations[conversation_identifier]

        sender = EmailSender(host=self.smtp_host, port=self.smtp_port)

        sender.send(
            subject=conversation.identifier,
            sender=self.sender_email,
            receivers=conversation.get_phone_numbers(),
            text=closing_text,
        )

    def send_message(
        self: TextNotifier,
        conversation_identifier: str,
        message: Message,
    ) -> None:
        conversation_identifier = conversation_identifier.replace(" ", "")

        if conversation_identifier not in self.conversations:
            raise RuntimeError("Conversation ID not recognized.")

        conversation = self.conversations[conversation_identifier]

        conversation.messages.append(message)

        sender = EmailSender(host=self.smtp_host, port=self.smtp_port)

        sender.send(
            subject=conversation.identifier,
            sender=self.sender_email,
            receivers=conversation.get_phone_numbers(),
            text=self._get_body(conversation, message),
        )
