from abc import abstractmethod

from ....Tools.AbstractClasses import InterfaceABC
from .InterfaceOptions.Transfer.TransferOptionsTracker import TransferOptionsTracker


class PipetteInterface(InterfaceABC):
    def __init__(self):
        pass

    @abstractmethod
    def Transfer(self, TransferOptionsTrackerInstance: TransferOptionsTracker):
        raise NotImplementedError
