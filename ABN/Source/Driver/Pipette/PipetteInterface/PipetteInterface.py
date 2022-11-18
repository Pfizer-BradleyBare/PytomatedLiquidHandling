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
    def Transfer50uL(self, TransferOptionsTrackerInstance: TransferOptionsTracker):
        raise NotImplementedError

    @abstractmethod
    def Transfer300uL(self, TransferOptionsTrackerInstance: TransferOptionsTracker):
        raise NotImplementedError

    @abstractmethod
    def Transfer1000uL(self, TransferOptionsTrackerInstance: TransferOptionsTracker):
        raise NotImplementedError

    @abstractmethod
    def MeasureLiquidHeight(
        self, TransferOptionsTrackerInstance: MeasureOptionsTracker
    ):
        raise NotImplementedError

    @abstractmethod
    def TipEject(self, TipOptionsTrackerInstance: TipOptionsTracker):
        raise NotImplementedError
