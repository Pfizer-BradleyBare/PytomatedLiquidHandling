from ...Tools.AbstractClasses import ObjectABC
from ..Labware import LabwareTracker
from ..Layout import LayoutItem


class Lid(ObjectABC):
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
