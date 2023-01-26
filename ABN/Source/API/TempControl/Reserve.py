from ...HAL.TempControlDevice.BaseTempControlDevice import TempControlDevice
from ...Server.Globals.HandlerRegistry import GetAPIHandler
from ..Tools.Container.BaseContainer import Container
from ..Tools.HALLayer.HALLayer import HALLayer
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Tools.ResourceLock.ResourceLockTracker import ResourceLockTracker


def Reserve(
    ContainerInstance: Container, Temperature: float, ShakingSpeed: int, Simulate: bool
) -> TempControlDevice | None:

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        GetAPIHandler().LoadedLabwareTrackerInstance  # type:ignore
    )

    HALLayerInstance: HALLayer = GetAPIHandler().HALLayerInstance  # type:ignore

    ResourceLockTrackerInstance: ResourceLockTracker = (
        GetAPIHandler().ResourceLockTrackerInstance  # type:ignore
    )

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(ContainerInstance)
    )

    if len(LoadedLabwareAssignmentInstances.GetObjectsAsList()) > 1:
        raise Exception(
            "There is more than one labware assignment for this Container. This must mean this is not a plate. Please Correct"
        )

    LabwareInstance = LoadedLabwareAssignmentInstances.GetObjectsAsList()[
        0
    ].LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance
    # Here we are getting the HAL labware of the plate we need to incubate/cool etc.

    if ShakingSpeed == 0:
        RequiresShaking = False
    else:
        RequiresShaking = True

    TempControlDeviceInstances = [
        Device
        for Device in HALLayerInstance.TempControlDeviceTrackerInstance.GetObjectsAsList()
        if not ResourceLockTrackerInstance.IsTracked(Device.GetName())
        and Device.ShakingSupported >= RequiresShaking
        and LabwareInstance
        in [
            LayoutItemInstance.PlateLayoutItemInstance.LabwareInstance
            for LayoutItemInstance in Device.SupportedLayoutItemGroupingTrackerInstance.GetObjectsAsList()
        ]
        and Temperature >= Device.TempLimitsInstance.MinimumTemp
        and Temperature <= Device.TempLimitsInstance.MaximumTemp
    ]
    # This is a big one. Not as complex as it looks:
    # 1. The device must not be tracked
    # 2. The device must only support shaking if we require shaking.
    # 3. The Labware of our Container must be supported by that device
    # 4 and 5. The temperature must fall within the support temp range of the device

    if len(TempControlDeviceInstances) == 0:
        return None
    # Nothing is available right now :(

    if Simulate is False:
        for TempControlDeviceInstance in TempControlDeviceInstances:
            TempControlDeviceInstance.UpdateCurrentTemperature()
    # Lets update the temperatures first

    BestFitDevice: TempControlDevice | None = None
    LowestTemperatureDifference = float("inf")

    for TempControlDeviceInstance in TempControlDeviceInstances:
        TemperatureDifference = abs(
            TempControlDeviceInstance.GetCurrentTemperature() - Temperature
        )

        if TemperatureDifference < LowestTemperatureDifference:
            LowestTemperatureDifference = TemperatureDifference
            BestFitDevice = TempControlDeviceInstance
    # Now we can find the device with the closest temperature

    if BestFitDevice is None:
        return None
    # Nothing is available right now :( same as above

    ResourceLockTrackerInstance.ManualLoad(BestFitDevice)

    if Simulate is False:
        BestFitDevice.SetTemperature(Temperature)

    return BestFitDevice
