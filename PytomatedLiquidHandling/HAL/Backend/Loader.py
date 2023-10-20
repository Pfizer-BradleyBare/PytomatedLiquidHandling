import os

import yaml
import logging

from PytomatedLiquidHandling.Driver.Hamilton.Backend import (
    MicrolabStarBackend,
    VantageBackend,
)
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import (
    BackendABC as BaseObject,
)
from PytomatedLiquidHandling.Driver.UnchainedLabs.Backend import StunnerBackend

Logger = logging.getLogger(__name__)

__Init: bool = False
__Objects: dict[str, BaseObject] = dict()


def GetObjects() -> dict[str, BaseObject]:
    if __Init:
        return __Objects
    else:
        raise RuntimeError(
            BaseObject.__name__ + " objects do not exist yet. Did you load them?"
        )


def Load(Dict: dict) -> dict[str, BaseObject]:
    global __Init
    __Init = True

    Logger.info("Loading Backend config yaml file.")

    for DeviceID in Dict:
        Device = Dict[DeviceID]
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

        __Objects[Identifier] = DeviceInstance

    return __Objects
