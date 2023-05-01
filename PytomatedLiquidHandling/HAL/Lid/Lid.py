from ...Tools.AbstractClasses import UniqueObjectABC
from ..Labware import LabwareTracker
from ..Layout import LayoutItem


class Lid(UniqueObjectABC):
    def __init__(
        self,
        UniqueIdentifier: str,
        LidLayoutItem: LayoutItem,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        self.UniqueIdentifier: str = UniqueIdentifier
        self.LidLayoutItem: LayoutItem = LidLayoutItem
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier
