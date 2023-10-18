import logging
import os

import yaml

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import BackendABC

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from . import HamiltonTipFTR, HamiltonTipNTR
from .Base import TipABC

Logger = logging.getLogger(__name__)


def LoadYaml(
    Backends: dict[str, BackendABC],
    FilePath: str,
) -> dict[str, TipABC]:
    Logger.info("Loading Tip config yaml file.")

    Tips: dict[str, TipABC] = dict()

    if not os.path.exists(FilePath):
        Logger.warning("Config file does not exist. Skipped")
        return Tips

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        Logger.warning(
            "Config file exists but does not contain any config items. Skipped"
        )
        return Tips

    for TipType in ConfigFile:
        for TipConfig in ConfigFile[TipType]:
            if TipConfig["Enabled"] == False:
                Logger.warning(
                    TipType
                    + " with unique ID "
                    + TipConfig["Unique Identifier"]
                    + " is not enabled so will be skipped."
                )
                continue

            Identifier = TipConfig["Identifier"]
            BackendInstance = Backends[TipConfig["Backend Identifier"]]
            CustomErrorHandling = TipConfig["Custom Error Handling"]

            LabwareIDs = TipConfig["Rack Layout Labware IDs"]
            MaxVolume = TipConfig["Volume"]

            if TipType == "Hamilton NTR":
                RackWasteLabwareID = TipConfig["Rack Waste Layout Labware ID"]
                GripperLabwareID = TipConfig["Gripper Layout Labware ID"]
                NumTiers = TipConfig["Number of Tiers"]
                TipsPerRack = TipConfig["Tips Per Rack"]

                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be a Hamilton Backend")

                TipInstance = HamiltonTipNTR(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    LabwareIDs,
                    MaxVolume,
                    NumTiers,
                    TipsPerRack,
                    RackWasteLabwareID,
                    GripperLabwareID,
                )

            elif TipType == "Hamilton FTR":
                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be a Hamilton Backend")

                TipInstance = HamiltonTipFTR(
                    Identifier,
                    BackendInstance,
                    CustomErrorHandling,
                    LabwareIDs,
                    MaxVolume,
                )

            else:
                raise Exception("Tip type not recognized")

            Tips[Identifier] = TipInstance

    return Tips
