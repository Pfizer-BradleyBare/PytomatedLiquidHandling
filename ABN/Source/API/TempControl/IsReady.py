from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice


def IsReady(TempControlDeviceInstance: TempControlDevice, Temperature: float):
    StableTempDelta = TempControlDeviceInstance.TempLimitsInstance.StableTempDelta

    TempControlDeviceInstance.UpdateCurrentTemperature()

    return (
        abs(TempControlDeviceInstance.GetCurrentTemperature() - Temperature)
        <= StableTempDelta
    )
