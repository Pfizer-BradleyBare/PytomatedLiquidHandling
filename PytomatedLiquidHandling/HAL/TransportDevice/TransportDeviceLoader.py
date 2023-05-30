import yaml

from ..Labware import LabwareTracker, PipettableLabware
from ..LayoutItem import LayoutItemTracker, NonCoverablePosition
from ..DeckLocation import DeckLocation
from ..TransportDevice import COREGripper, InternalPlateGripper, TrackGripper
from .BaseTransportDevice import (
    TransportableLabware,
    TransportableLabwareTracker,
    TransportDeviceTracker,
    TransportParameters,
)
from ..Backend import BackendTracker
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Backend import VantageBackend


def LoadYaml(
    BackendTrackerInstance: BackendTracker,
    LabwareTrackerInstance: LabwareTracker,
    FilePath: str,
) -> TransportDeviceTracker:
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    FillerDeckLocationInstance = DeckLocation("TransitionPoint", None)  # type:ignore
    # This filler is only used so we can create a layout item. The deck location info will never actually be used

    TransitionPoints = ConfigFile["Transition Points"]

    TransitionPointTrackerInstance = LayoutItemTracker()

    for TransitionPoint in TransitionPoints:
        if TransitionPoint["Enabled"] == False:
            continue

        PlateSequence = TransitionPoint["Plate Sequence"]
        PlateLabwareInstance = LabwareTrackerInstance.GetObjectByName(
            TransitionPoint["Plate Sequence"]
        )

        if not isinstance(PlateLabwareInstance, PipettableLabware):
            raise Exception("This should never happen")

        TransitionPointTrackerInstance.LoadSingle(
            NonCoverablePosition(
                str(PlateLabwareInstance.GetUniqueIdentifier()),
                PlateSequence,
                PlateLabwareInstance,
                FillerDeckLocationInstance,
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
        for LabwareID in Device["Supported Labware"]:
            LabwareObject = LabwareTrackerInstance.GetObjectByName(LabwareID)

            CloseOffset = Device["Supported Labware"][LabwareID]["Close Offset"]
            OpenOffset = Device["Supported Labware"][LabwareID]["Open Offset"]
            PickupHeight = Device["Supported Labware"][LabwareID]["Pickup Height"]

            Parameters = TransportParameters(CloseOffset, OpenOffset, PickupHeight)

            TransportableLabwareTrackerInstance.LoadSingle(
                TransportableLabware(LabwareObject, Parameters)
            )

        if DeviceType == "CORE Gripper":
            GripperSequence = Device["Gripper Sequence"]

            if not isinstance(BackendInstance, HamiltonBackendABC):
                raise Exception("Backend not correct. Must be of Hamilton backend type")

            TransportDeviceTrackerInstance.LoadSingle(
                COREGripper(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    TransportableLabwareTrackerInstance,
                    GripperSequence,
                )
            )

        elif DeviceType == "Internal Plate Gripper":
            if not isinstance(BackendInstance, HamiltonBackendABC):
                raise Exception("Backend not correct. Must be of Hamilton backend type")

            TransportDeviceTrackerInstance.LoadSingle(
                InternalPlateGripper(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    TransportableLabwareTrackerInstance,
                )
            )

        elif DeviceType == "Track Gripper":
            if not isinstance(BackendInstance, VantageBackend):
                raise Exception("Backend not correct. Must be of Vantage backend type")

            TransportDeviceTrackerInstance.LoadSingle(
                TrackGripper(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    TransportableLabwareTrackerInstance,
                )
            )

    return TransportDeviceTrackerInstance
