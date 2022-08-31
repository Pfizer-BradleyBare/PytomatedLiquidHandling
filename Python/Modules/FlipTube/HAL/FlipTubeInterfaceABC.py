from abc import abstractmethod, ABC
from ...ABC import InterfaceABC


class FlipTubeInterfaceABC(ABC, InterfaceABC):
    @abstractmethod
    def HALFlipTubeOpen(self):
        raise NotImplementedError

    @abstractmethod
    def HALFlipTubeClose(self):
        raise NotImplementedError
