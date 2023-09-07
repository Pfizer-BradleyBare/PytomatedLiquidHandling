import os

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

from ...Tools.Logger import Logger
from .Base import (
    DeckLocationTransportConfig,
    DeckLocationTransportConfigTracker,
    TransportDeviceTracker,
)
from .HamiltonCOREGripper import HamiltonCOREGripper
from .HamiltonInternalPlateGripper import HamiltonInternalPlateGripper
from .VantageTrackGripper import VantageTrackGripper


def LoadYaml(
    LoggerInstance: Logger,
    BackendTrackerInstance: Backend.BackendTracker,
    LabwareTrackerInstance: Labware.LabwareTracker,
    DeckLocationTrackerInstance: DeckLocation.DeckLocationTracker,
    FilePath: str,
) -> TransportDeviceTracker:
    LoggerInstance.info("Loading TransportDevice config yaml file.")

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return TransportDeviceTracker(LayoutItem.LayoutItemTracker())

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return TransportDeviceTracker(LayoutItem.LayoutItemTracker())

    FillerDeckLocationInstance = DeckLocation.DeckLocation(
        "TransitionPoint",
        DeckLocation.CarrierConfig(Carrier.NonMoveableCarrier("", 0, 0, 0, "", ""), 0),
    )
    # This filler is only used so we can create a layout item. The deck location info will never actually be used

    TransitionPoints = ConfigFile["Transition Points"]

    TransitionPointTrackerInstance = LayoutItem.LayoutItemTracker()

    for TransitionPoint in TransitionPoints:
        if TransitionPoint["Enabled"] == False:
            LoggerInstance.warning(
                "Transition Point for labware "
                + TransitionPoint["Plate Labware Unique Identifier"]
                + " is not enabled so will be skipped."
            )
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
            LoggerInstance.warning(
                DeviceType
                + " with unique ID "
                + Device["Unique Identifier"]
                + " is not enabled so will be skipped."
            )
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

            if DeviceType == "Hamilton CORE Gripper":
                GetConfigInstance = HamiltonCOREGripper.GetConfig(GetConfig)
                PlaceConfigInstance = HamiltonCOREGripper.PlaceConfig(PlaceConfig)
            elif DeviceType == "Hamilton Internal Plate Gripper":
                GetConfigInstance = HamiltonInternalPlateGripper.GetConfig(GetConfig)
                PlaceConfigInstance = HamiltonInternalPlateGripper.PlaceConfig(
                    PlaceConfig
                )
            elif DeviceType == "Vantage Track Gripper":
                GetConfigInstance = VantageTrackGripper.GetConfig(GetConfig)
                PlaceConfigInstance = VantageTrackGripper.PlaceConfig(PlaceConfig)
            else:
                raise Exception("Device type not recognized")

            DeckLocationTransportConfigTrackerInstance.LoadSingle(
                DeckLocationTransportConfig(
                    DeckLocationID, GetConfigInstance, PlaceConfigInstance
                )
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
