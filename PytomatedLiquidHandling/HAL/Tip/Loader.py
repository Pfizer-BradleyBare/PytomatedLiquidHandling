import os

import yaml

from PytomatedLiquidHandling.HAL import Backend

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Tools.Logger import Logger
from . import HamiltonTipFTR, HamiltonTipNTR
from .BaseTip import TipTracker


def LoadYaml(
    LoggerInstance: Logger,
    BackendTrackerInstance: Backend.BackendTracker,
    FilePath: str,
) -> TipTracker:
    TipTrackerInstance = TipTracker()

    if not os.path.exists(FilePath):
        LoggerInstance.warning("Tip config file does not exist.")
        return TipTrackerInstance

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    if ConfigFile is None:
        LoggerInstance.warning(
            "Tip config file exists but does not contain any config items"
        )
        return TipTrackerInstance

    for TipType in ConfigFile:
        for Tip in ConfigFile[TipType]:
            if Tip["Enabled"] == False:
                continue

            UniqueIdentifier = Tip["Unique Identifier"]
            BackendInstance = BackendTrackerInstance.GetObjectByName(
                Tip["Backend Unique Identifier"]
            )
            CustomErrorHandling = Tip["Custom Error Handling"]

            PickupSequence = Tip["Pickup Sequence"]
            MaxVolume = Tip["Volume"]

            if TipType == "Hamilton NTR":
                NTRWasteSequence = Tip["NTR Waste Sequence"]
                GripperSequence = Tip["Gripper Sequence"]

                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be a Hamilton Backend")

                TipInstance = HamiltonTipNTR(
                    UniqueIdentifier,
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
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    PickupSequence,
                    MaxVolume,
                )

            else:
                raise Exception("Tip type not recognized")

            TipTrackerInstance.LoadSingle(TipInstance)

    return TipTrackerInstance
