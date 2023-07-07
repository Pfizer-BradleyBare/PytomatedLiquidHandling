from abc import ABC, abstractmethod
from dataclasses import dataclass

from .....Tools.AbstractClasses import UniqueObjectABC


@dataclass
class DeckLocationTransportConfig(UniqueObjectABC):
    class TransportConfigABC(ABC):
        def __eq__(self, __value: object) -> bool:
            if not isinstance(__value, self.__class__):
                return False

            for Key in self._ComparisonKeys():
                if vars(self)[Key] != vars(__value)[Key]:
                    return False

            return True

        @abstractmethod
        def __init__(self, Config: dict):
            self.Config: dict = Config

        @abstractmethod
        def _ComparisonKeys(self) -> list[str]:
            ...

    GetConfig: TransportConfigABC
    PlaceConfig: TransportConfigABC
