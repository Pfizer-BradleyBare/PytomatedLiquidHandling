from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..DeckLocation.MoveToPipette import MoveToPipette
from ..Tools.Labware.BaseLabware import Labware as APILabware


def End(
    APILabwareInstance: APILabware,
    TempControlDeviceInstance: TempControlDevice,
):

    TempControlDeviceInstance.SetTemperature(25)
    TempControlDeviceInstance.StopShaking()

    MoveToPipette(APILabwareInstance)
