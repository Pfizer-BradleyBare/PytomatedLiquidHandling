import yaml

from ...Driver.Hamilton.Backend import MicrolabStarBackend, VantageBackend
from ...Driver.UnchainedLabs.Backend import StunnerBackend
from ...Tools.Logger import Logger
from .BackendTracker import BackendTracker


def LoadYaml(LoggerInstance: Logger, FilePath: str) -> BackendTracker:
    BackendTrackerInstance = BackendTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for DeviceID in ConfigFile:
        Device = ConfigFile[DeviceID]
        UniqueID = Device["Unique Identifier"]

        if DeviceID == "Microlab Star":
            DeviceInstance = MicrolabStarBackend(
                UniqueID, LoggerInstance, Device["Deck Layout Path"]
            )
        elif DeviceID == "Vantage":
            DeviceInstance = VantageBackend(
                UniqueID, LoggerInstance, Device["Deck Layout Path"]
            )
        elif DeviceID == "Stunner":
            DeviceInstance = StunnerBackend(
                UniqueID, LoggerInstance, Device["IP Address"], Device["Port"]
            )
        else:
            raise Exception("Device not recognized")

        BackendTrackerInstance.LoadSingle(DeviceInstance)

    return BackendTrackerInstance
