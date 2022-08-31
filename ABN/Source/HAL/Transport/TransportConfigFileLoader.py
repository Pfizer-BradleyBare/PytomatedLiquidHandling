import yaml
from .Transport import (
    TransportParameters,
    TransportableLabware,
    TransportDevices,
    COREGripperDevice,
)
from .TransportTracker import TransportTracker


def LoadYaml(TransportTrackerInstance: TransportTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for DeviceID in ConfigFile["Device IDs"]:

        DeviceConfig = ConfigFile["Device IDs"][DeviceID]

        if DeviceConfig["Supported Labware"] is None:
            continue

        Labwares = list()
        for LabwareID in DeviceConfig["Supported Labware"]:
            LabwareObject = (
                TransportTrackerInstance.LabwareTrackerInstance.GetObjectByName(
                    LabwareID
                )
            )

            CloseOffset = DeviceConfig["Supported Labware"][LabwareID]["Close Offset"]
            OpenOffset = DeviceConfig["Supported Labware"][LabwareID]["Open Offset"]
            PickupHeight = DeviceConfig["Supported Labware"][LabwareID]["Pickup Height"]

            Parameters = TransportParameters(CloseOffset, OpenOffset, PickupHeight)

            Labwares.append(TransportableLabware(LabwareObject, Parameters))

        TransportDevice = TransportDevices(DeviceID)
        if TransportDevice == TransportDevices.COREGripper:
            GripperSequence = DeviceConfig["Gripper Sequence"]
            TransportTrackerInstance.LoadManual(
                COREGripperDevice(Labwares, GripperSequence)
            )

        elif TransportDevice == TransportDevices.InternalPlateGripper:
            pass

        elif TransportDevice == TransportDevices.TrackGripper:
            pass
