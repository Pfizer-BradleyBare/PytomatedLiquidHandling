from enum import Enum

from ....Tools.AbstractClasses import ObjectABC
from ...Labware import LabwareTracker
from .Interface.ClosedContainerInterface import ClosedContainerInterface


class ClosedContainerTypes(Enum):
    FlipTube = "FlipTube"


class ClosedContainer(ObjectABC, ClosedContainerInterface):
    def __init__(
        self,
        Type: ClosedContainerTypes,
        ToolSequence: str,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        self.Type: ClosedContainerTypes = Type
        self.ToolSequence: str = ToolSequence
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    def GetName(self) -> str:
        return self.Type.value
