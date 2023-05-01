from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Labware import LabwareTracker
from .Interface.ClosedContainerInterface import ClosedContainerInterface


class ClosedContainerTypes(Enum):
    HamiltonFlipTube = "Hamilton FlipTube"


class ClosedContainer(UniqueObjectABC, ClosedContainerInterface):
    def __init__(
        self,
        Name: str,
        ToolSequence: str,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        self.Name: str = Name
        self.ToolSequence: str = ToolSequence
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    def GetName(self) -> str:
        return self.Name
