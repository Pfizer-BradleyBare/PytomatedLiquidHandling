from ....Tools.AbstractClasses import UniqueObjectABC
from ...Labware import LabwareTracker
from ...DeckLocation import DeckLocationTracker
from ...Tools.AbstractClasses import InterfaceABC
from ....Driver.Tools.AbstractClasses import BackendABC
from .Interface import OpenCloseOptions
from abc import abstractmethod
from dataclasses import dataclass


@dataclass
class ClosedContainerABC(InterfaceABC, UniqueObjectABC):
    ToolSequence: str
    SupportedDeckLocationTrackerInstance: DeckLocationTracker
    SupportedLabwareTrackerInstance: LabwareTracker

    @abstractmethod
    def Open(self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker):
        ...

    @abstractmethod
    def Close(
        self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker
    ):
        ...
