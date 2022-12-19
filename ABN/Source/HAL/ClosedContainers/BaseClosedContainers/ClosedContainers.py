from enum import Enum

from ....Tools.AbstractClasses import ObjectABC
from ...Labware import LabwareTracker
from .Interface.ClosedContainersInterface import ClosedContainersInterface


class ClosedContainersTypes(Enum):
    FlipTube = "FlipTube"


class ClosedContainers(ObjectABC, ClosedContainersInterface):
    def __init__(
        self,
        Type: ClosedContainersTypes,
        ToolSequence: str,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        self.Type: ClosedContainersTypes = Type
        self.ToolSequence: str = ToolSequence
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    def GetName(self) -> str:
        return self.Type.value
