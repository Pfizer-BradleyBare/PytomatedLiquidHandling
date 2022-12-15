from abc import abstractmethod

from .....Tools.AbstractClasses import InterfaceABC
from .TransferOptions.TransferOptionsTracker import TransferOptionsTracker


class PipetteInterface(InterfaceABC):
    TipsStored: bool = False

    def __init__(self):
        pass

    @abstractmethod
    def Transfer(self, TransferOptionsTrackerInstance: TransferOptionsTracker):
        raise NotImplementedError
