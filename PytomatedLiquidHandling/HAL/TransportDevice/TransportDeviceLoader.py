import yaml

from ..Labware import LabwareTracker
from ..TransportDevice import COREGripper, InternalPlateGripper, TrackGripper
from .BaseTransportDevice import (
    TransportableLabware,
    TransportableLabwareTracker,
    TransportDeviceTracker,
    TransportParameters,
)


def LoadYaml(
    LabwareTrackerInstance: LabwareTracker, FilePath: str
) -> TransportDeviceTracker:
    TransportDeviceTrackerInstance = TransportDeviceTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for DeviceType in ConfigFile:
        Device = ConfigFile[DeviceType]

        if Device["Enabled"] == False:
            continue

        UniqueIdentifier = Device["Unique Identifier"]
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
            TransportDeviceTrackerInstance.LoadSingle(
                COREGripper(
                    UniqueIdentifier,
                    CustomErrorHandling,
                    TransportableLabwareTrackerInstance,
                    GripperSequence,
                )
            )

        elif DeviceType == "Internal Plate Gripper":
            TransportDeviceTrackerInstance.LoadSingle(
                InternalPlateGripper(
                    UniqueIdentifier,
                    CustomErrorHandling,
                    TransportableLabwareTrackerInstance,
                )
            )

        elif DeviceType == "Track Gripper":
            TransportDeviceTrackerInstance.LoadSingle(
                TrackGripper(
                    UniqueIdentifier,
                    CustomErrorHandling,
                    TransportableLabwareTrackerInstance,
                )
            )

    return TransportDeviceTrackerInstance
