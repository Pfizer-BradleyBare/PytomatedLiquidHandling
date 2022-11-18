from enum import Enum

from ...Tools.AbstractClasses import ObjectABC
from .PipetteTip.PipetteTipTracker import PipetteTipTracker


class PipettingDeviceTypes(Enum):
    Pipette8Channel = "1mL Channels Portrait"
    Pipette96Channel = "96 Core Head"


class Pipette(ObjectABC):
    def __init__(
        self,
        PipettingDeviceType: PipettingDeviceTypes,
        Enabled: bool,
        SupoortedPipetteTipTrackerInstance: PipetteTipTracker,
    ):
        self.PipettingDeviceType: PipettingDeviceTypes = PipettingDeviceType
        self.Enabled: bool = Enabled
        self.SupoortedPipetteTipTrackerInstance: PipetteTipTracker = (
            SupoortedPipetteTipTrackerInstance
        )

    def GetName(self) -> str:
        return self.PipettingDeviceType.value

    def IsEnabled(self) -> bool:
        return self.Enabled

    def GetSupoortedPipetteTipTracker(self) -> PipetteTipTracker:
        return self.SupoortedPipetteTipTrackerInstance


class Pipette96Channel(Pipette):
    def __init__(
        self,
        Enabled: bool,
        SupoortedPipetteTipTrackerInstance: PipetteTipTracker,
    ):
        Pipette.__init__(
            self,
            PipettingDeviceTypes.Pipette96Channel,
            Enabled,
            SupoortedPipetteTipTrackerInstance,
        )


class Pipette8Channel(Pipette):
    def __init__(
        self,
        Enabled: bool,
        SupoortedPipetteTipTrackerInstance: PipetteTipTracker,
        ActiveChannels: list[int],
    ):
        Pipette.__init__(
            self,
            PipettingDeviceTypes.Pipette8Channel,
            Enabled,
            SupoortedPipetteTipTrackerInstance,
        )
        self.ActiveChannels: list[int] = ActiveChannels
