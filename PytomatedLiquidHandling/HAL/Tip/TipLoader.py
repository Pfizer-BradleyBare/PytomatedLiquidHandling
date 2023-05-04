import yaml

from ..Tip import TipFTR, TipNTR
from .BaseTip import TipTracker, TipTypes


def LoadYaml(FilePath: str) -> TipTracker:
    TipTrackerInstance = TipTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for TipID in ConfigFile["Tip IDs"]:
        TipItem = ConfigFile["Tip IDs"][TipID]

        if TipItem["Enabled"] is True:
            PickupSequence = TipItem["Pickup Sequence"]
            MaxVolume = TipItem["Volume"]

            TipType = TipTypes(TipItem["Tip Type"])

            if TipType == TipTypes.NTR:
                NTRWasteSequence = TipItem["NTR Waste Sequence"]
                GripperSequence = TipItem["Gripper Sequence"]

                TipTrackerInstance.LoadSingle(
                    TipNTR(
                        TipID,
                        PickupSequence,
                        NTRWasteSequence,
                        GripperSequence,
                        MaxVolume,
                    )
                )

            elif TipType == TipTypes.FTR or TipType == TipTypes.FTRSlim:
                TipTrackerInstance.LoadSingle(TipFTR(TipID, PickupSequence, MaxVolume))

    return TipTrackerInstance
