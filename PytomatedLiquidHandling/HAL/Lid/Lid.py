from ...Tools.AbstractClasses import UniqueObjectABC
from ..Labware import LabwareTracker
from ..Layout import LayoutItem


class Lid(UniqueObjectABC):
    def __init__(
        self,
        Name: str,
        LidLayoutItem: LayoutItem,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        self.Name: str = Name
        self.LidLayoutItem: LayoutItem = LidLayoutItem
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    def GetName(self) -> str:
        return self.Name
