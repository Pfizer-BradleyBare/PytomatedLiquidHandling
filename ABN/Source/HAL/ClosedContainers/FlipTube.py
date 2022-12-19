from ..Labware import LabwareTracker
from .BaseClosedContainers.ClosedContainers import (
    ClosedContainers,
    ClosedContainersTypes,
)


class FlipTube(ClosedContainers):
    def __init__(
        self, ToolSequence: str, SupportedLabwareTrackerInstance: LabwareTracker
    ):
        ClosedContainers.__init__(
            self,
            ClosedContainersTypes.FlipTube,
            ToolSequence,
            SupportedLabwareTrackerInstance,
        )
