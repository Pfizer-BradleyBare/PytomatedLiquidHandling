from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import DeckLocation, Labware
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Tools.AbstractClasses import InterfaceABC
from .Interface import OpenCloseOptions


@dataclass
class ClosedContainerABC(InterfaceABC, UniqueObjectABC):
    ToolSequence: str
    SupportedDeckLocationTrackerInstance: DeckLocation.DeckLocationTracker
    SupportedLabwareTrackerInstance: Labware.LabwareTracker

    @abstractmethod
    def Open(self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker):
        ...

    @abstractmethod
    def Close(
        self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker
    ):
        ...
