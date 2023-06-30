import yaml

from PytomatedLiquidHandling.Driver.Hamilton.Backend import (
    HamiltonBackendABC,
    VantageBackend,
)
from PytomatedLiquidHandling.HAL import (
    Backend,
    Carrier,
    DeckLocation,
    Labware,
    LayoutItem,
)

from . import HamiltonCOREGripper, HamiltonInternalPlateGripper, VantageTrackGripper
from .BaseTransportDevice import (
    TransportableLabware,
    TransportableLabwareTracker,
    TransportDeviceTracker,
    TransportParameters,
)


def LoadYaml(
    BackendTrackerInstance: Backend.BackendTracker,
    LabwareTrackerInstance: Labware.LabwareTracker,
    FilePath: str,
) -> TransportDeviceTracker:
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    FillerDeckLocationInstance = DeckLocation.DeckLocation(
        "TransitionPoint",
        DeckLocation.CarrierConfig(
            Carrier.NonMoveableCarrier("", "", 0, 0, 0, "", ""), 0
        ),
        DeckLocation.TransportDeviceConfig("", {}, {}, {}, {}),
    )
    # This filler is only used so we can create a layout item. The deck location info will never actually be used

    TransitionPoints = ConfigFile["Transition Points"]

    TransitionPointTrackerInstance = LayoutItem.LayoutItemTracker()

    for TransitionPoint in TransitionPoints:
        if TransitionPoint["Enabled"] == False:
            continue

        PlateSequence = TransitionPoint["Plate Sequence"]
        PlateLabwareInstance = LabwareTrackerInstance.GetObjectByName(
            TransitionPoint["Plate Labware Unique Identifier"]
        )

        if not isinstance(PlateLabwareInstance, Labware.PipettableLabware):
            raise Exception("This should never happen")

        TransitionPointTrackerInstance.LoadSingle(
            LayoutItem.NonCoverableItem(
                str(PlateLabwareInstance.UniqueIdentifier),
                PlateSequence,
                FillerDeckLocationInstance,
                PlateLabwareInstance,
            )
        )

    TransportDeviceTrackerInstance = TransportDeviceTracker(
        TransitionPointTrackerInstance
    )
    # load the transition points

    del ConfigFile["Transition Points"]

    for DeviceType in ConfigFile:
        Device = ConfigFile[DeviceType]

        if Device["Enabled"] == False:
            continue

        UniqueIdentifier = Device["Unique Identifier"]
        BackendInstance = BackendTrackerInstance.GetObjectByName(
            Device["Backend Unique Identifier"]
        )
        CustomErrorHandling = Device["Custom Error Handling"]

        TransportableLabwareTrackerInstance = TransportableLabwareTracker()
        for LabwareInformation in Device["Supported Labware Information"]:
            LabwareObject = LabwareTrackerInstance.GetObjectByName(
                LabwareInformation["Labware Unique Identifier"]
            )

            CloseOffset = LabwareInformation["Close Offset"]
            OpenOffset = LabwareInformation["Open Offset"]
            PickupHeight = LabwareInformation["Pickup Height"]

            Parameters = TransportParameters(CloseOffset, OpenOffset, PickupHeight)

            TransportableLabwareTrackerInstance.LoadSingle(
                TransportableLabware(LabwareObject, Parameters)
            )

        if DeviceType == "Hamilton CORE Gripper":
            GripperSequence = Device["Gripper Sequence"]

            if not isinstance(BackendInstance, HamiltonBackendABC):
                raise Exception("Backend not correct. Must be of Hamilton backend type")

            TransportDeviceTrackerInstance.LoadSingle(
                HamiltonCOREGripper(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    TransportableLabwareTrackerInstance,
                    GripperSequence,
                )
            )

        elif DeviceType == "Hamilton Internal Plate Gripper":
            if not isinstance(BackendInstance, HamiltonBackendABC):
                raise Exception("Backend not correct. Must be of Hamilton backend type")

            TransportDeviceTrackerInstance.LoadSingle(
                HamiltonInternalPlateGripper(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    TransportableLabwareTrackerInstance,
                )
            )

        elif DeviceType == "Vantage Track Gripper":
            if not isinstance(BackendInstance, VantageBackend):
                raise Exception("Backend not correct. Must be of Vantage backend type")

            TransportDeviceTrackerInstance.LoadSingle(
                VantageTrackGripper(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    TransportableLabwareTrackerInstance,
                )
            )

    return TransportDeviceTrackerInstance
