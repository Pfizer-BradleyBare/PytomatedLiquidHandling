import yaml

from ..Tip import TipFTR, TipNTR
from .BaseTip import TipTracker, TipTypes


def LoadYaml(TipTrackerInstance: TipTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for TipID in ConfigFile["Tip IDs"]:
        TipItem = ConfigFile["Tip IDs"][TipID]

        if TipItem["Enabled"] is True:
            PickupSequence = TipItem["Pickup Sequence"]
            MaxVolume = TipItem["Max Pipetting Volume"]

            TipType = TipTypes(TipItem["Tip Type"])

            if TipType == TipTypes.NTR:
                NTRWasteSequence = TipItem["NTR Waste Sequence"]
                GripperSequence = TipItem["Gripper Sequence"]

                TipTrackerInstance.ManualLoad(
                    TipNTR(
                        TipID,
                        PickupSequence,
                        NTRWasteSequence,
                        GripperSequence,
                        MaxVolume,
                    )
                )

            elif TipType == TipTypes.FTR:
                TipTrackerInstance.ManualLoad(TipFTR(TipID, PickupSequence, MaxVolume))
