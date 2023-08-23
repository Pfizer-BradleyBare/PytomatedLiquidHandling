import os

import yaml

from PytomatedLiquidHandling.HAL import Backend

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Tools.Logger import Logger
from . import HamiltonTipFTR, HamiltonTipNTR
from .BaseTip import Tip
from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC


def LoadYaml(
    LoggerInstance: Logger,
    Backends: dict[str, BackendABC],
    FilePath: str,
) -> dict[str, Tip]:
    LoggerInstance.info("Loading Tip config yaml file.")

    Tips: dict[str, Tip] = dict()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Config file does not exist. Skipped")
        return Tips

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return Tips

    for TipType in ConfigFile:
        for TipConfig in ConfigFile[TipType]:
            if TipConfig["Enabled"] == False:
                LoggerInstance.warning(
                    TipType
                    + " with unique ID "
                    + TipConfig["Unique Identifier"]
                    + " is not enabled so will be skipped."
                )
                continue

            Identifier = TipConfig["Identifier"]
            BackendInstance = Backends[TipConfig["Backend Identifier"]]
            CustomErrorHandling = TipConfig["Custom Error Handling"]

            PickupSequence = TipConfig["Pickup Sequence"]
            MaxVolume = TipConfig["Volume"]

            if TipType == "Hamilton NTR":
                NTRWasteSequence = TipConfig["NTR Waste Sequence"]
                GripperSequence = TipConfig["Gripper Sequence"]

                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be a Hamilton Backend")

                TipInstance = HamiltonTipNTR(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    PickupSequence,
                    MaxVolume,
                    NTRWasteSequence,
                    GripperSequence,
                )

            elif TipType == "Hamilton FTR":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be a Hamilton Backend")

                TipInstance = HamiltonTipFTR(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    PickupSequence,
                    MaxVolume,
                )

            else:
                raise Exception("Tip type not recognized")

            Tips[Identifier] = TipInstance

    return Tips
