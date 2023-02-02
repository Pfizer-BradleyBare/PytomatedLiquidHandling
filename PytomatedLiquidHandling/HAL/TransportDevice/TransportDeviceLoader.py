import yaml

from ..Labware import LabwareTracker
from ..TransportDevice import COREGripper, InternalPlateGripper, TrackGripper
from .BaseTransportDevice import (
    TransportableLabware,
    TransportableLabwareTracker,
    TransportDevices,
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

    for DeviceID in ConfigFile["Device IDs"]:

        DeviceConfig = ConfigFile["Device IDs"][DeviceID]

        if DeviceConfig["Enabled"] is True:

            TransportableLabwareTrackerInstance = TransportableLabwareTracker()
            for LabwareID in DeviceConfig["Supported Labware"]:
                LabwareObject = LabwareTrackerInstance.GetObjectByName(LabwareID)

                CloseOffset = DeviceConfig["Supported Labware"][LabwareID][
                    "Close Offset"
                ]
                OpenOffset = DeviceConfig["Supported Labware"][LabwareID]["Open Offset"]
                PickupHeight = DeviceConfig["Supported Labware"][LabwareID][
                    "Pickup Height"
                ]

                Parameters = TransportParameters(CloseOffset, OpenOffset, PickupHeight)

                TransportableLabwareTrackerInstance.ManualLoad(
                    TransportableLabware(LabwareObject, Parameters)
                )

            TransportDevice = TransportDevices(DeviceID)
            if TransportDevice == TransportDevices.COREGripper:
                GripperSequence = DeviceConfig["Gripper Sequence"]
                TransportDeviceTrackerInstance.ManualLoad(
                    COREGripper(TransportableLabwareTrackerInstance, GripperSequence)
                )

            elif TransportDevice == TransportDevices.InternalPlateGripper:
                TransportDeviceTrackerInstance.ManualLoad(
                    InternalPlateGripper(TransportableLabwareTrackerInstance)
                )

            elif TransportDevice == TransportDevices.TrackGripper:
                TransportDeviceTrackerInstance.ManualLoad(
                    TrackGripper(TransportableLabwareTrackerInstance)
                )

    return TransportDeviceTrackerInstance
