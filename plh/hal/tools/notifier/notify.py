from __future__ import annotations

import dataclasses
import datetime

from .contacts import ContactInfo
from .response import ResponseEnum

id_counter = 0


@dataclasses.dataclass(kw_only=True)
class NotificationMetaData:
    id: int = dataclasses.field(init=False)
    contacts: ContactInfo
    subject: str
    body: str
    response_options: type[ResponseEnum]

    @dataclasses.dataclass(kw_only=True)
    class ResponseTracker:
        time: datetime.datetime
        response_body: ResponseEnum

    responses: list[ResponseTracker]

    def __post_init__(self: NotificationMetaData) -> None:
        global id_counter
        id_counter = id_counter + 1
        self.id = id_counter


def notify(subject: str, body: str, response_options: type[ResponseEnum] | None) -> int:
    ...


def get_response(id: int) -> ResponseEnum:
    ...
