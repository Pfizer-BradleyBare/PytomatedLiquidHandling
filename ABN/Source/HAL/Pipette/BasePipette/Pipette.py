from enum import Enum

from ....Tools.AbstractClasses import ObjectABC
from ...Labware import LabwareTracker
from .Interface.PipetteInterface import PipetteInterface
from .PipetteTip.PipetteTipTracker import PipetteTipTracker


class PipettingDeviceTypes(Enum):
    Pipette8Channel = "1mL Channels Portrait"
    Pipette96Channel = "96 Core Head"


class Pipette(ObjectABC, PipetteInterface):
    def __init__(
        self,
        PipettingDeviceType: PipettingDeviceTypes,
        Enabled: bool,
        SupoortedPipetteTipTrackerInstance: PipetteTipTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
    ):
        self.PipettingDeviceType: PipettingDeviceTypes = PipettingDeviceType
        self.Enabled: bool = Enabled
        self.SupoortedPipetteTipTrackerInstance: PipetteTipTracker = (
            SupoortedPipetteTipTrackerInstance
        )
        self.SupportedLabwareTrackerInstance: LabwareTracker = (
            SupportedLabwareTrackerInstance
        )

    def GetName(self) -> str:
        return self.PipettingDeviceType.value

    def IsEnabled(self) -> bool:
        return self.Enabled

    def GetSupoortedPipetteTipTracker(self) -> PipetteTipTracker:
        return self.SupoortedPipetteTipTrackerInstance
