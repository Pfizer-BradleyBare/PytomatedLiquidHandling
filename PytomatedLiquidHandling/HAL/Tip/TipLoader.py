import yaml

from ..Tip import HamiltonTipNTR, HamiltonTipFTR
from .BaseTip import TipTracker
from ..Backend import BackendTracker
from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC


def LoadYaml(FilePath: str, BackendTrackerInstance: BackendTracker) -> TipTracker:
    TipTrackerInstance = TipTracker()

    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

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

            if TipType == "NTR":
                NTRWasteSequence = Tip["NTR Waste Sequence"]
                GripperSequence = Tip["Gripper Sequence"]

                if not isinstance(BackendInstance, HamiltonBackendABC):
                    raise Exception("Must be a Hamilton Backend")

                TipInstance = HamiltonTipNTR(
                    UniqueIdentifier,
                    BackendInstance,
                    CustomErrorHandling,
                    PickupSequence,
                    NTRWasteSequence,
                    GripperSequence,
                    MaxVolume,
                )

            elif TipType == "FTR":
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
