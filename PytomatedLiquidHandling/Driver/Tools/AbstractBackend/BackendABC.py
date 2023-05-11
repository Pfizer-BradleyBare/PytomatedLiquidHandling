from abc import ABC, abstractmethod
from typing import Any


class BackendABC(ABC):
    @abstractmethod
    def StartBackend(self):
        ...

    @abstractmethod
    def StopBackend(self):
        ...

    @abstractmethod
    def GetRawStatus(self) -> int:
        ...

    @abstractmethod
    def SendCommand(self, CommandParams: dict[str, Any]):
        ...

    @abstractmethod
    def ResponseReady(self) -> bool:
        ...

    @abstractmethod
    def GetResponse(self) -> dict[str, list[Any]]:
        ...
