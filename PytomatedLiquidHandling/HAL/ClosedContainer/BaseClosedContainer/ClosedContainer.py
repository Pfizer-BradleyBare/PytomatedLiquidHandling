from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Labware import LabwareTracker
from .Interface.ClosedContainerInterface import ClosedContainerInterface


class ClosedContainerTypes(Enum):
    HamiltonFlipTube = "Hamilton FlipTube"


class ClosedContainer(UniqueObjectABC, ClosedContainerInterface):
    def __init__(
        self,
        UniqueIdentifier: str,
        ToolSequence: str,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        self.UniqueIdentifier: str = UniqueIdentifier
        self.ToolSequence: str = ToolSequence
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    def GetUniqueIdentifier(self) -> str:
        return self.UniqueIdentifier
