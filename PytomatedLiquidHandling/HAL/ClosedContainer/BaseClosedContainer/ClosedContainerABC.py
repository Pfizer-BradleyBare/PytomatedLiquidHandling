from ....Tools.AbstractClasses import UniqueObjectABC
from ...Labware import LabwareTracker
from ...DeckLocation import DeckLocationTracker
from ...Tools.AbstractClasses import InterfaceABC
from ....Driver.Tools.AbstractClasses import BackendABC
from .Interface import OpenCloseOptions
from abc import abstractmethod


class ClosedContainerABC(UniqueObjectABC, InterfaceABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        BackendInstance: BackendABC,
        CustomErrorHandling: bool,
        ToolSequence: str,
        SupportedDeckLocationTrackerInstance: DeckLocationTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        InterfaceABC.__init__(self, BackendInstance, CustomErrorHandling)
        self.ToolSequence: str = ToolSequence
        self.SupportedDeckLocationTrackerInstance: DeckLocationTracker = (
            SupportedDeckLocationTrackerInstance
        )
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    @abstractmethod
    def Open(self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker):
        ...

    @abstractmethod
    def Close(
        self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker
    ):
        ...
