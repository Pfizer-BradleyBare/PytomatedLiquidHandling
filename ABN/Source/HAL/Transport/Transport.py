from enum import Enum
from ..Labware import Labware
from ...AbstractClasses import ObjectABC


class TransportParameters:
    def __init__(self, CloseOffset: float, OpenOffset: float, PickupHeight: float):
        self.CloseOffset: float = CloseOffset
        self.OpenOffset: float = OpenOffset
        self.PickupHeight: float = PickupHeight

    def GetCloseOffset(self) -> float:
        return self.CloseOffset

    def GetOpenOffset(self) -> float:
        return self.OpenOffset

    def GetPickupHeight(self) -> float:
        return self.PickupHeight


class TransportableLabware:
    def __init__(self, LabwareInstance: Labware, Parameters: TransportParameters):
        self.Name: str = LabwareInstance.GetName()
        self.LabwareObject: Labware = LabwareInstance
        self.Parameters: TransportParameters = Parameters

    def GetName(self) -> str:
        return self.Name

    def GetLabware(self) -> Labware:
        return self.LabwareObject

    def GetTransportParameters(self) -> TransportParameters:
        return self.Parameters


class TransportDevices(Enum):
    COREGripper = "CORE Gripper"
    InternalPlateGripper = "Internal Plate Gripper"
    TrackGripper = "Track Gripper"


class TransportDevice(ObjectABC):
    def __init__(
        self,
        TransportDeviceID: TransportDevices,
        SupportedLabware: list[TransportableLabware],
    ):
        self.SupportedLabware: list[TransportableLabware] = SupportedLabware
        self.TransportDeviceID: TransportDevices = TransportDeviceID

    def GetName(self) -> str:
        return self.TransportDeviceID.value

    def GetSupportedLabware(self) -> list[TransportableLabware]:
        return self.SupportedLabware

    def GetTransportDevice(self) -> TransportDevices:
        return self.TransportDeviceID


class COREGripperDevice(TransportDevice):
    def __init__(
        self, SupportedLabware: list[TransportableLabware], GripperSequence: str
    ):
        self.GripperSequence: str = GripperSequence
        TransportDevice.__init__(self, TransportDevices.COREGripper, SupportedLabware)

    def GetGripperSequence(self) -> str:
        return self.GripperSequence


class IternalPlateGripperDevice(TransportDevice):
    def __init__(self, SupportedLabware: list[TransportableLabware]):
        TransportDevice.__init__(
            self, TransportDevices.InternalPlateGripper, SupportedLabware
        )


class TrackGripperDevice(TransportDevice):
    def __init__(self, SupportedLabware: list[TransportableLabware]):
        TransportDevice.__init__(
            self, TransportDevices.InternalPlateGripper, SupportedLabware
        )
