from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ..Tools.RunTypes import RunTypes


def IsReady(
    TempControlDeviceInstance: TempControlDevice, Temperature: float, RunType: RunTypes
) -> bool:
    StableTempDelta = TempControlDeviceInstance.TempLimitsInstance.StableTempDelta

    if not RunType is RunTypes.Run:
        return True

    TempControlDeviceInstance.UpdateCurrentTemperature()

    return (
        abs(TempControlDeviceInstance.GetCurrentTemperature() - Temperature)
        <= StableTempDelta
    )
