from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..DeckLocation.MoveToPipette import MoveToPipette
from ..Tools.Container.BaseContainer import Container
from ..Tools.RunTypes import RunTypes


def End(
    ContainerInstance: Container,
    TempControlDeviceInstance: TempControlDevice,
    RunType: RunTypes,
):

    if RunType is RunTypes.Run:
        TempControlDeviceInstance.SetTemperature(25)
        TempControlDeviceInstance.StopShaking()

    MoveToPipette(ContainerInstance, RunType)
