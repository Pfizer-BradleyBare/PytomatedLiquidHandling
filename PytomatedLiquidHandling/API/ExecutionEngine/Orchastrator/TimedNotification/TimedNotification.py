from dataclasses import dataclass, field

from ..Timer import Timer


@dataclass
class TimedNotification(Timer):
    Message: str
