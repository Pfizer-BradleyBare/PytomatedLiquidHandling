from ...Tools.AbstractClasses import ObjectABC
from ..Labware import LabwareTracker


class FlipTube(ObjectABC):
    def __init__(
        self, Name: str, Sequence: str, SupportedLabwareTrackerInstance: LabwareTracker
    ):
        self.Name: str = Name
        self.Sequence: str = Sequence
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    def GetName(self) -> str:
        return self.Name
