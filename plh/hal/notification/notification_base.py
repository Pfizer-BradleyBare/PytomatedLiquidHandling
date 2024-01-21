from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import dataclasses

from plh.hal.tools import HALDevice


@dataclasses.dataclass
class NotificationBase(HALDevice, ABC):
    @abstractmethod
    def placeholder(self):
        ...
