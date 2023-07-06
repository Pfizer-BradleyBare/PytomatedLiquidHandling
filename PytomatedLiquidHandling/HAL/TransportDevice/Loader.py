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
    DeckLocationTransportConfig,
    DeckLocationTransportConfigTracker,
    TransportDeviceTracker,
)


def LoadYaml(
    BackendTrackerInstance: Backend.BackendTracker,
    LabwareTrackerInstance: Labware.LabwareTracker,
    DeckLocationTrackerInstance: DeckLocation.DeckLocationTracker,
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

        SupportedLabwareTrackerInstance = Labware.LabwareTracker()
        for LabwareID in Device["Supported Labware Unique Identifiers"]:
            LabwareInstance = LabwareTrackerInstance.GetObjectByName(LabwareID)

            SupportedLabwareTrackerInstance.LoadSingle(LabwareInstance)

        DeckLocationTransportConfigTrackerInstance = (
            DeckLocationTransportConfigTracker()
        )
        for DeckLocationConfig in Device["Supported Deck Locations Config"]:
            DeckLocationID = DeckLocationConfig["Deck Location Unique Identifier"]

            DeckLocationTrackerInstance.GetObjectByName(DeckLocationID)
            # Does this deck location exist?

            GetConfig = DeckLocationConfig["Get Configuration"]
            PlaceConfig = DeckLocationConfig["Place Configuration"]

            DeckLocationTransportConfigTrackerInstance.LoadSingle(
                DeckLocationTransportConfig(DeckLocationID, GetConfig, PlaceConfig)
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
                    DeckLocationTransportConfigTrackerInstance,
                    SupportedLabwareTrackerInstance,
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
                    DeckLocationTransportConfigTrackerInstance,
                    SupportedLabwareTrackerInstance,
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
                    DeckLocationTransportConfigTrackerInstance,
                    SupportedLabwareTrackerInstance,
                )
            )

    return TransportDeviceTrackerInstance
