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
class EmailMessage(Message):
    to: list[str]
    message_id: str
    references: list[str]


@dataclasses.dataclass(kw_only=True)
class EmailConversation(ConversationBase):
    messages: list[EmailMessage] = field(init=False, default_factory=list)
    contacts: list[EmailContact]


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


    def _send_to_all(self: EmailNotifier, conversation:EmailConversation, text:str) -> None:
        """This just sends a message to all contacts using the latest message ID and reference info.
        This does NOT create a message in the conversation."""
        messages = conversation.messages

        messages.reverse()
        # Reverse the messages so we can find the last message for each contact.

        contact_message: dict[str, EmailMessage] = {}

        for contact in self.default_contacts + conversation.contacts:
            email = contact.email

            for message in messages:
                if email in message.to:
                    contact_message[email] = message
                    break
        # Find the latest message for all contacts.

        sender = EmailSender(host=self.smtp_host, port=self.smtp_port)

        with sender:
            for contact, message in contact_message.items():
                sender.send(
                    subject=conversation.identifier,
                    sender=self.sender_email,
                    receivers=contact,
                    headers={
                        "Message-ID": f"{sender.create_message_id()}",
                        "References": f"{' '.join(message.references)} {message.message_id}",
                    },
                    text=text,
                )
        #send the message.


    def start_conversation(
        self: EmailNotifier,
        identifier: str,
        opening_text: str,
        contacts: list[ContactInfoBase],
        response_options: type[ConversationResponseOptionsEnumBase] = ConversationResponseOptionsEnumBase,
    ) -> None:
        if identifier in self.conversations:
            raise RuntimeError("Conversation already exists.")

        conversation = EmailConversation(
            identifier=identifier,
            contacts=[
                contact for contact in contacts if isinstance(contact, EmailContact)
            ],
            response_options=response_options,
        )

        self.conversations[identifier] = conversation
        # create the conversation

        sender = EmailSender(host=self.smtp_host, port=self.smtp_port)

        default_receivers = [contact.email for contact in self.default_contacts]
        extra_receivers = [contact.email for contact in conversation.contacts]
        # get our starting recievers!

        message = EmailMessage(
            subject=opening_text,
            extra_text="",
            response_options=MessageResponseOptionsEnumBase,
            to=default_receivers + extra_receivers,
            message_id=sender.create_message_id(),
            references=[],
        )
        # Create the message. We will use the message id to help us manage email threads.
        # Our message subject will be an initial line.
        # Extra text is a following remark with more info.

        conversation.messages.append(message)

        if len(message.response_options) > 0:
            newline = "\n"
            message.extra_text = f"""{message.extra_text} You may send the following responses to this message only:

{newline.join([f"'{i.name}' for {i.value}" for i in message.response_options])}

"""
        ###If message response options are possible then deal with that.

        if len(conversation.response_options) > 0:
            newline = "\n"
            message.extra_text = f"""{message.extra_text} You may send the following responses at any time to get more information:

{newline.join([f"'{i.name}' for {i.value}" for i in conversation.response_options])}

"""
        ###If conversation response options are possible then deal with that.

        message.extra_text = f"""{message.extra_text} Thanks!"""

        self._send_to_all(conversation,f"{message.subject}\n\n{message.extra_text}")

    def end_conversation(
        self: EmailNotifier,
        identifier: str,
        closing_text: str,
    ) -> None:
        if identifier not in self.conversations:
            return

        conversation = self.conversations[identifier]

        del self.conversations[identifier]

        self._send_to_all(conversation,closing_text)
        #close out.

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

    def get_conversation_response(self: NotifierBase, conversation_identifier: str) -> ConversationResponseOptionsEnumBase | None:
        return super().get_conversation_response(conversation_identifier)

    def get_message_response(self: NotifierBase, conversation_identifier: str, message: Message) -> MessageResponseOptionsEnumBase | None:
        return super().get_message_response(conversation_identifier, message)

    def _response_monitor(self: EmailNotifier) -> None:
        inbox = EmailBox(
            host=self.inbox_host,
            port=self.inbox_port,
            username=self.sender_username,
            password=self.sender_password,
        )["INBOX"]

        while True:
            for redbox_message in inbox.search(unseen=True):
                redbox_message.delete()
                # Immediately delete the message to keep the inbox clean.

                message = mailparser.parse_from_string("".join(redbox_message.content))
                # Parse the message. Redbox parsing is not good enough.

                from_ = message.from_[0][1]
                subject = str(message.subject)

                body = message.body[:message.body.find("-----Original Message-----")].replace(" ","").replace("\n","")
                #Strip everything from body except for a potential command.

                try:
                    references = [
                        *message.headers["References"].split("\n "),
                        message.headers["Message-ID"],
                    ]
                except KeyError:
                    references = []
                #References are super important.
                #Basically we use this information to tell email software the conversation thread.

                if "Returned mail" in subject or "Warning" in subject:
                    continue
                # skip returned mail for bad emails. Who knows if it will happen but best to ignore.

                try:
                    conversation = self.conversations[subject.replace("RE: ", "")]
                except KeyError:
                    sender = EmailSender(self.smtp_host, self.smtp_port)

                    sender.send(
                        subject=subject,
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
                    continue
                # try to find the associated waiting notification.

                try:
                    conversation.response = conversation.response_options[body]
                    continue
                except KeyError:
                    ...
                #try to parse into conversation options if available


                #try to parse into message options if available

            time.sleep(1)
