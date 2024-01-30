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

        conversation = EmailConversation(
            identifier=identifier,
            contacts=[
                contact for contact in contacts if isinstance(contact, EmailContact)
            ]
            + self.default_contacts,
            response_options=response_options,
            reference=sender.create_message_id(),
        )

        self.conversations[identifier] = conversation
        # create the conversation

        message = Message(
            subject=opening_text,
            extra_text=None,
            response_options=MessageResponseOptionsEnumBase,
        )
        # Create the message. We will use the message id to help us manage email threads.
        # Our message subject will be an initial line.
        # Extra text is a following remark with more info.

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

    def get_conversation_response(
        self: NotifierBase,
        conversation_identifier: str,
    ) -> ConversationResponseOptionsEnumBase | None:
        return super().get_conversation_response(conversation_identifier)

    def get_message_response(
        self: NotifierBase,
        conversation_identifier: str,
        message: Message,
    ) -> MessageResponseOptionsEnumBase | None:
        return super().get_message_response(conversation_identifier, message)

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

                message = mailparser.parse_from_string("".join(redbox_message.content))
                # Parse the message. Redbox parsing is not good enough.

                from_ = message.from_[0][1]
                subject = str(message.subject)

                body = (
                    message.body[: message.body.find("-----Original Message-----")]
                    .replace(" ", "")
                    .replace("\n", "")
                )
                # Strip everything from body except for a potential command.

                try:
                    references = [
                        *message.headers["References"].split("\n "),
                        message.headers["Message-ID"],
                    ]
                except KeyError:
                    references = []
                # References are super important.
                # Basically we use this information to tell email software the conversation thread.

                if "Returned mail" in subject or "Warning" in subject:
                    continue
                # skip returned mail for bad emails. Who knows if it will happen but best to ignore.

                try:
                    conversation = self.conversations[subject.replace("RE: ", "")]
                except KeyError:
                    sender.send(
                        subject=subject,
                        sender=self.sender_email,
                        receivers=from_,
                        headers={
                            "Message-ID": f"{sender.create_message_id()}",
                            "References": f"{' '.join(references)}",
                        },
                        text=(
                            """The conversation subject line you used was not recognized.
Make sure you use the subject line that was sent to you (RE: is OK).

NOTE: If you know you used the correct subject line but still received this message then the conversation may have ended. Thus, responses are no longer accepted.

Thanks!"""
                        ),
                    )
                    continue
                # try to find the associated waiting notification.

                response_message = Message(
                    subject=conversation.identifier,
                    extra_text=None,
                )

                try:
                    conversation.response = conversation.response_options[body]

                    sender.send(
                        subject=conversation.identifier,
                        sender=self.sender_email,
                        receivers=from_,
                        headers={
                            "Message-ID": f"{sender.create_message_id()}",
                            "References": f"{' '.join(references)}",
                        },
                        text="""The conversation subject line you used was not recognized.
Make sure you use the subject line that was sent to you (RE: is OK).
Please try again.
NOTE: If you know you used the correct subject line then the conversation may have ended. Thus, responses are no longer accepted.

Thanks!""",
                    )
                except KeyError:
                    ...
                # try to parse into conversation options if available

                # try to parse into message options if available

            time.sleep(1)
