import os

import yaml

from ...Driver.Hamilton.Backend import MicrolabStarBackend, VantageBackend
from ...Driver.UnchainedLabs.Backend import StunnerBackend
from ...Tools.Logger import Logger
from .BackendTracker import BackendTracker


def LoadYaml(LoggerInstance: Logger, FilePath: str) -> BackendTracker:
    LoggerInstance.info("Loading Backend config yaml file.")

    BackendTrackerInstance = BackendTracker()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return BackendTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return BackendTrackerInstance

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
