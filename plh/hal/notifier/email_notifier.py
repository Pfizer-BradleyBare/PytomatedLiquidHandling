from __future__ import annotations

import threading
import time
from dataclasses import field

import mailparser
from pydantic import dataclasses
from redbox import EmailBox
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
class EmailContact(ContactInfoBase):
    email: str


@dataclasses.dataclass(kw_only=True)
class EmailConversation(ConversationBase):
    contacts: list[EmailContact]
    reference: str

    def get_emails(self: EmailConversation) -> list[str]:
        return [contact.email for contact in self.contacts]


@dataclasses.dataclass(kw_only=True)
class EmailNotifier(NotifierBase):
    smtp_host: str
    smtp_port: int
    inbox_host: str
    inbox_port: int
    sender_email: str
    sender_username: str
    sender_password: str

    default_contacts: list[EmailContact]

    conversations: dict[str, EmailConversation] = field(
        init=False,
        default_factory=dict,
    )

    def start_conversation(
        self: EmailNotifier,
        identifier: str,
        opening_text: str,
        contacts: list[ContactInfoBase],
        response_options: type[
            ConversationResponseOptionsEnumBase
        ] = ConversationResponseOptionsEnumBase,
    ) -> None:
        if identifier in self.conversations:
            raise RuntimeError("Conversation already exists.")

        sender = EmailSender(host=self.smtp_host, port=self.smtp_port)

        message = Message(
            subject=opening_text,
            extra_text=None,
            response_options=MessageResponseOptionsEnumBase,
        )
        # Create the message. We will use the message id to help us manage email threads.
        # Our message subject will be an initial line.
        # Extra text is a following remark with more info.

        conversation = EmailConversation(
            identifier=identifier,
            contacts=[
                contact for contact in contacts if isinstance(contact, EmailContact)
            ]
            + self.default_contacts,
            latest_message=message,
            response_options=response_options,
            reference=sender.create_message_id(),
        )

        self.conversations[identifier.replace(" ", "")] = conversation
        # create the conversation

        conversation.messages.append(message)

        sender.send(
            subject=conversation.identifier,
            sender=self.sender_email,
            receivers=conversation.get_emails(),
            headers={"Message-ID": conversation.reference},
            text=message.get_body(conversation.response_options),
        )

    def end_conversation(
        self: EmailNotifier,
        identifier: str,
        closing_text: str,
    ) -> None:
        if identifier not in self.conversations:
            return

        conversation = self.conversations[identifier]

        del self.conversations[identifier]

        sender = EmailSender(host=self.smtp_host, port=self.smtp_port)

        sender.send(
            subject=conversation.identifier,
            sender=self.sender_email,
            receivers=conversation.get_emails(),
            headers={"References": conversation.reference},
            text=closing_text,
        )

    def __post_init__(self: EmailNotifier) -> None:
        threading.Thread(
            name="EmailTextNotifier Response Monitor",
            target=self._response_monitor,
            daemon=True,
        ).start()

    def send_message(
        self: NotifierBase,
        conversation_identifier: str,
        message: Message,
    ) -> None:
        return super().send_message(conversation_identifier, message)

    def _response_monitor(self: EmailNotifier) -> None:
        inbox = EmailBox(
            host=self.inbox_host,
            port=self.inbox_port,
            username=self.sender_username,
            password=self.sender_password,
        )["INBOX"]

        sender = EmailSender(self.smtp_host, self.smtp_port)

        while True:
            for redbox_message in inbox.search(unseen=True):
                redbox_message.delete()
                # Immediately delete the message to keep the inbox clean.

                parsed_message = mailparser.parse_from_string(
                    "".join(redbox_message.content),
                )
                # Parse the message. Redbox parsing is not good enough.

                from_ = parsed_message.from_[0][1]
                subject = str(parsed_message.subject)

                if "Returned mail" in subject or "Warning" in subject:
                    continue
                # skip returned mail for bad emails. Who knows if it will happen but best to ignore.

                try:
                    conversation = self.conversations[
                        subject.replace("RE:", "").replace(" ", "")
                    ]
                except KeyError:

                    text = ""
                    text += (
                        "The conversation subject line you used was not recognized.\n"
                    )
                    text += "Make sure you use the subject line that was sent to you (RE: is OK).\n"
                    text += "NOTE: If you know you used the correct subject line then the conversation may have ended."
                    text += "Thus, responses are no longer accepted.\n\n"
                    text += "Thanks!"

                    sender.send(
                        subject=subject,
                        sender=self.sender_email,
                        receivers=from_,
                        headers={
                            "References": parsed_message.headers["Message-ID"],
                        },
                        text=text,
                    )
                    continue
                # try to find the associated conversation.

                body = (
                    parsed_message.body[
                        : parsed_message.body.find("-----Original Message-----")
                    ]
                    .replace(" ", "")
                    .replace("\n", "")
                )
                # Strip everything from body except for a potential command.

                try:
                    conversation.response = conversation.response_options[body]
                    continue
                except KeyError:
                    ...
                # try to parse into conversation options if available

                latest_message = conversation.latest_message

                try:
                    response = latest_message.response_options[body]

                    if latest_message.response is not None:
                        text = ""
                        text += "Latest message already has a response:\n\n"
                        text += f"{latest_message.response.name} -> {latest_message.response.value}\n\n"
                        text += "Thanks!"

                        sender.send(
                            subject=subject,
                            sender=self.sender_email,
                            receivers=from_,
                            headers={
                                "References": conversation.reference,
                            },
                            text=text,
                        )

                    latest_message.response = response
                    continue
                except KeyError:
                    ...
                # try to parse into message options if available

                text = ""
                text += "Response not recognized. As a reminder:\n\n"
                text += latest_message.get_responses_body(conversation.response_options)
                text += "\n"
                text += "Thanks!"

                sender.send(
                    subject=subject,
                    sender=self.sender_email,
                    receivers=from_,
                    headers={
                        "References": conversation.reference,
                    },
                    text=text,
                )

            time.sleep(1)
