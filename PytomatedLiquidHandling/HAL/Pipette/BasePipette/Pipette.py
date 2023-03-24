from enum import Enum

from ....Tools.AbstractClasses import UniqueObjectABC
from ...Labware import LabwareTracker
from .Interface.PipetteInterface import PipetteInterface
from .PipetteTip.PipetteTipTracker import PipetteTipTracker


class PipettingDeviceTypes(Enum):
    Pipette8Channel = "1mL Channels Portrait"
    Pipette96Channel = "96 Core Head"


class Pipette(UniqueObjectABC, PipetteInterface):
    def __init__(
        self,
        PipettingDeviceType: PipettingDeviceTypes,
        Enabled: bool,
        SupportedPipetteTipTrackerInstance: PipetteTipTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        self.PipettingDeviceType: PipettingDeviceTypes = PipettingDeviceType
        self.Enabled: bool = Enabled
        self.SupportedPipetteTipTrackerInstance: PipetteTipTracker = (
            SupportedPipetteTipTrackerInstance
        )
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    def GetName(self) -> str:
        return self.PipettingDeviceType.value
