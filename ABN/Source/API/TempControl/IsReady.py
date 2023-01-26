from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice


def IsReady(
    TempControlDeviceInstance: TempControlDevice, Temperature: float, Simulate: bool
) -> bool:
    StableTempDelta = TempControlDeviceInstance.TempLimitsInstance.StableTempDelta

    if Simulate is True:
        return True

    TempControlDeviceInstance.UpdateCurrentTemperature()

    return (
        abs(TempControlDeviceInstance.GetCurrentTemperature() - Temperature)
        <= StableTempDelta
    )
