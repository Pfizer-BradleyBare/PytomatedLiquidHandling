from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..DeckLocation.MoveToPipette import MoveToPipette
from ..Tools.Container.BaseContainer import Container


def End(
    ContainerInstance: Container,
    TempControlDeviceInstance: TempControlDevice,
):

    TempControlDeviceInstance.SetTemperature(25)
    TempControlDeviceInstance.StopShaking()

    MoveToPipette(ContainerInstance)
