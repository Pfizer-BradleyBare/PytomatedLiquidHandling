from collections import defaultdict

from ..Labware import LabwareTracker
from ..Pipette import TransferOptionsTracker
from .BasePipette import Pipette, PipetteTipTracker, PipettingDeviceTypes
from .BasePipette.Interface.PipetteInterface import (
    TestLabwareSupported,
    TestSumLessThanMax,
)


class Pipette8Channel(Pipette):
    def __init__(
        self,
        Enabled: bool,
        SupoortedPipetteTipTrackerInstance: PipetteTipTracker,
        SupportedLabwareTrackerInstance: LabwareTracker,
        ActiveChannels: list[int],
    ):
        Pipette.__init__(
            self,
            PipettingDeviceTypes.Pipette8Channel,
            Enabled,
            SupoortedPipetteTipTrackerInstance,
            SupportedLabwareTrackerInstance,
        )
        self.ActiveChannels: list[int] = ActiveChannels

    def Initialize(self):
        pass

    def Deinitialize(self):
        pass

    def Transfer(self, TransferOptionsTrackerInstance: TransferOptionsTracker):
        pass

        TransferOptionDict = defaultdict(list)

        for TransferOption in TransferOptionsTrackerInstance.GetObjectsAsList():
            TempDict = vars(TransferOption)

            for key, value in TempDict.items():
                TransferOptionDict[key].append(value)
        # Covert options to dict of lists of transfer option

        MaxVolumes = [
            Volume - 0 for Volume in TransferOptionDict["CurrentSourceVolume"]
        ]

        if (
            len(
                TestSumLessThanMax(
                    TransferOptionDict["SourceLayoutItemInstance"],
                    TransferOptionDict["SourcePosition"],
                    TransferOptionDict["TransferVolume"],
                    MaxVolumes,
                )
            )
            != 0
        ):
            raise Exception(
                "There is not enough valume left in your source containers. TODO add more info"
            )
        # Does each source contain enough volume for this transfer?

        MaxVolumes = [
            Volume - 0 for Volume in TransferOptionDict["CurrentDestinationVolume"]
        ]

        if (
            len(
                TestSumLessThanMax(
                    TransferOptionDict["DestinationLayoutItemInstance"],
                    TransferOptionDict["DestinationPosition"],
                    TransferOptionDict["TransferVolume"],
                    MaxVolumes,
                )
            )
            != 0
        ):
            raise Exception(
                "There is not enough valume left in your source containers. TODO add more info"
            )
        # Can the destination accomodate the liquid?

        if (
            len(
                TestLabwareSupported(
                    self.SupportedLabwareTrackerInstance,
                    TransferOptionDict["SourceLayoutItemInstance"],
                )
            )
            != 0
        ):
            raise Exception(
                "This device does not support the labware of your source layout item. TODO add more info"
            )

        if (
            len(
                TestLabwareSupported(
                    self.SupportedLabwareTrackerInstance,
                    TransferOptionDict["DestinationLayoutItemInstance"],
                )
            )
            != 0
        ):
            raise Exception(
                "This device does not support the labware of your destination layout item. TODO add more info"
            )
        # Are the source and destination items labware supported by this device?

        # Is the source and destintion in a correct pipetting deck location? TODO

        NumActiveChannels = len(self.ActiveChannels)
        NumTransfers = TransferOptionsTrackerInstance.GetNumObjects()

        PipettingChannels = (
            self.ActiveChannels * (int(NumTransfers / NumActiveChannels) + 1)
        )[:NumTransfers]
        # Do some array math to align the active channels across our transfers

        # Now the pipetting junk. aye yi yi
