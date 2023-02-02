from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..DeckLocation.MoveToPipette import MoveToPipette
from ..Tools.Container.BaseContainer import Container


def End(
    ContainerInstance: Container,
    TempControlDeviceInstance: TempControlDevice,
    Simulate: bool,
):

    if Simulate is False:
        TempControlDeviceInstance.SetTemperature(25)
        TempControlDeviceInstance.StopShaking()

    MoveToPipette(ContainerInstance, Simulate)
