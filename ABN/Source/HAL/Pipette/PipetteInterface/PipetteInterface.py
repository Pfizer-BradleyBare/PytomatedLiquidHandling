from abc import abstractmethod

from ....Tools.AbstractClasses import InterfaceABC
from .Options.MeasureOptions.MeasureOptionsTracker import MeasureOptionsTracker
from .Options.TipOptions.TipOptionsTracker import TipOptionsTracker
from .Options.TransferOptions.TransferOptionsTracker import TransferOptionsTracker


class PipetteInterface(InterfaceABC):
    @abstractmethod
    def TipPickup(self, TipOptionsTrackerInstance: TipOptionsTracker):
        raise NotImplementedError

    @abstractmethod
    def Transfer(self, TransferOptionsTrackerInstance: TransferOptionsTracker):
        raise NotImplementedError

    @abstractmethod
    def TipEject(self, TipOptionsTrackerInstance: TipOptionsTracker):
        raise NotImplementedError
