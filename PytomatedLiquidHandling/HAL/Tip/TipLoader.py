import yaml

from ..Tip import TipFTR, TipNTR
from .BaseTip import TipTracker, TipTypes


def LoadYaml(FilePath: str) -> TipTracker:
    TipTrackerInstance = TipTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for Tip in ConfigFile:
        if Tip["Enabled"] == False:
            continue

        UniqueIdentifier = Tip["Unique Identifier"]
        CustomErrorHandling = Tip["Custom Error Handling"]
        TipType = Tip["Tip Type"]

        PickupSequence = Tip["Pickup Sequence"]
        MaxVolume = Tip["Volume"]

        if TipType == "NTR":
            NTRWasteSequence = Tip["NTR Waste Sequence"]
            GripperSequence = Tip["Gripper Sequence"]

            TipInstance = TipNTR(
                UniqueIdentifier,
                CustomErrorHandling,
                PickupSequence,
                NTRWasteSequence,
                GripperSequence,
                MaxVolume,
            )

        elif TipType == "FTR":
            TipInstance = TipFTR(
                UniqueIdentifier, CustomErrorHandling, PickupSequence, MaxVolume
            )

        else:
            raise Exception("Tip type not recognized")

        TipTrackerInstance.LoadSingle(TipInstance)

    return TipTrackerInstance
