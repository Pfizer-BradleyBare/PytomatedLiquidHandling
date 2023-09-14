import os

import yaml
import logging

from PytomatedLiquidHandling.Driver.Hamilton.Backend import (
    MicrolabStarBackend,
    VantageBackend,
)
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC
from PytomatedLiquidHandling.Driver.UnchainedLabs.Backend import StunnerBackend

Logger = logging.getLogger(__name__)


def LoadYaml(FilePath: str) -> dict[str, BackendABC]:
    Logger.info("Loading Backend config yaml file.")

    Backends: dict[str, BackendABC] = dict()

    if not os.path.exists(FilePath):
        Logger.warning("Config file does not exist. Skipped")
        return Backends

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        Logger.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return Backends

    for DeviceID in ConfigFile:
        Device = ConfigFile[DeviceID]
        Identifier = Device["Identifier"]

        if DeviceID == "Microlab Star":
            DeviceInstance = MicrolabStarBackend(Identifier, Device["Deck Layout Path"])
        elif DeviceID == "Vantage":
            DeviceInstance = VantageBackend(Identifier, Device["Deck Layout Path"])
        elif DeviceID == "Stunner":
            DeviceInstance = StunnerBackend(
                Identifier, Device["IP Address"], Device["Port"]
            )
        else:
            raise Exception("Device not recognized")

        Backends[Identifier] = DeviceInstance

    return Backends
