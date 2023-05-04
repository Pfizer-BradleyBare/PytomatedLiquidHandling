from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Labware import LabwareTracker
from .Interface.ClosedContainerInterface import ClosedContainerInterface


class ClosedContainer(UniqueObjectABC, ClosedContainerInterface):
    def __init__(
        self,
        UniqueIdentifier: str,
        ToolSequence: str,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.ToolSequence: str = ToolSequence
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )
