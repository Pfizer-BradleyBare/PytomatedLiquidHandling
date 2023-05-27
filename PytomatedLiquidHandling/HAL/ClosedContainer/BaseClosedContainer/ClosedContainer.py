from ....Tools.AbstractClasses import UniqueObjectABC
from ...Labware import LabwareTracker
from ...DeckLocation import DeckLocationTracker
from .Interface.ClosedContainerInterface import ClosedContainerInterface
from ....Driver.Tools.AbstractClasses import BackendABC


class ClosedContainer(UniqueObjectABC, ClosedContainerInterface):
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
        ClosedContainerInterface.__init__(self, BackendInstance, CustomErrorHandling)
        self.ToolSequence: str = ToolSequence
        self.SupportedDeckLocationTrackerInstance: DeckLocationTracker = (
            SupportedDeckLocationTrackerInstance
        )
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )
