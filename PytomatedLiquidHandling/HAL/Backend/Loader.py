import os

import yaml

from PytomatedLiquidHandling.Driver.Hamilton.Backend import (
    MicrolabStarBackend,
    VantageBackend,
)
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.Driver.UnchainedLabs.Backend import StunnerBackend
from PytomatedLiquidHandling.Tools.Logger import Logger


def LoadYaml(LoggerInstance: Logger, FilePath: str) -> dict[str, BackendABC]:
    LoggerInstance.info("Loading Backend config yaml file.")

    Backends: dict[str, BackendABC] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return Backends

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return Backends

    for DeviceID in ConfigFile:
        Device = ConfigFile[DeviceID]
        Identifier = Device["Identifier"]

        if DeviceID == "Microlab Star":
            DeviceInstance = MicrolabStarBackend(
                Identifier, LoggerInstance, Device["Deck Layout Path"]
            )
        elif DeviceID == "Vantage":
            DeviceInstance = VantageBackend(
                Identifier, LoggerInstance, Device["Deck Layout Path"]
            )
        elif DeviceID == "Stunner":
            DeviceInstance = StunnerBackend(
                Identifier, LoggerInstance, Device["IP Address"], Device["Port"]
            )
        else:
            raise Exception("Device not recognized")

        Backends[Identifier] = DeviceInstance

    return Backends
