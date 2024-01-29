from __future__ import annotations

import threading
import time

import mailparser
from pydantic import dataclasses
from redbox import EmailBox
from redmail.email.sender import EmailSender

from .contact_info_base import *
from .contact_info_base import ContactInfoBase
from .notifier_base import *
from .notifier_base import NotifierBase
from .response_base import *
from .response_base import ResponseOptionsEnumBase

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
    emails: list[str] | None


@dataclasses.dataclass(kw_only=True)
class EmailNotifier(NotifierBase):
    host: str
    sender: str

    default_contacts: list[EmailContact]

    def _response_monitor(self) -> None:
        inbox = EmailBox(
            host="imap.pfizer.com",
            port=993,
            username="",
            password="",
        )["INBOX"]

        while True:
            for message in inbox.search(unseen=True):
                message.delete()
                # Immediately delete the message to keep the inbox clean.

                print(message.content)

                message = mailparser.parse_from_string("".join(message.content))
                # Parse the message. Redbox parsing is not good enough.

                from_ = message.from_[0][1]
                subject = message.subject
                body = message.body

                if subject == "Returned mail: see transcript for details":
                    print("ignored returned mail.")
                    continue
                # skip returned mail for bad phone numbers. We brute force the numbers so it will definitely happen.

                notifications = [
                    notification
                    for notification in self.active_notifications.values()
                    if subject
                    == f"{notification.subject} -> {self.identifier}:{notification.id}"
                ]
                # try to find the associated waiting notification.

            time.sleep(1)

    def __post_init__(self: EmailNotifier) -> None:
        threading.Thread(
            name="EmailTextNotifier Response Monitor",
            target=self._response_monitor,
            daemon=True,
        ).start()

    def notify(
        self: EmailNotifier,
        contacts: list[ContactInfoBase],
        id: int,
        subject: str,
        body: str,
        response_options: type[ResponseOptionsEnumBase] | None,
    ) -> None:
        super().notify(contacts, id, subject, body, response_options)

        email = EmailSender(host=self.host, port=0)

        filtered_contacts = [
            contact for contact in contacts if isinstance(contact, EmailContact)
        ]

        emails = sum(
            [
                contact.emails
                for contact in filtered_contacts
                if contact.emails is not None
            ],
            [],
        )
        # Extract the emails portion of the contacts.

        if response_options is not None:
            newline = "\n"
            body = f"""{body}

The following response options are available:
(Please respond with the text before the colon ':')

{newline.join([f"{i.name}: {i.value}" for i in response_options])}

Thanks!"""

        email.send(
            subject=f"{subject} -> {self.identifier}:{id}",
            sender=self.sender,
            receivers=emails,
            text=body,
        )
