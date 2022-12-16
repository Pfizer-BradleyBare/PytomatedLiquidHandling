from collections import defaultdict
from math import ceil

from ...Driver.Pipette.Pipette8Channel import (
    AspirateCommand,
    AspirateOptions,
    AspirateOptionsTracker,
    DispenseCommand,
    DispenseOptions,
    DispenseOptionsTracker,
    EjectCommand,
    EjectOptions,
    EjectOptionsTracker,
    PickupCommand,
    PickupOptions,
    PickupOptionsTracker,
)
from ...Driver.Tools import CommandTracker
from ..Labware import LabwareTracker
from ..Pipette import TransferOptionsTracker
from .BasePipette import Pipette, PipetteTip, PipetteTipTracker, PipettingDeviceTypes
from .BasePipette.Interface.PipetteInterface import (
    ClampMax,
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

        SourceLayoutItemInstances = [
            Option.SourceLayoutItemInstance
            for Option in TransferOptionsTrackerInstance.GetObjectsAsList()
        ]
        SourcePositions = [
            Option.SourcePosition
            for Option in TransferOptionsTrackerInstance.GetObjectsAsList()
        ]
        CurrentSourceVolumes = [
            Option.CurrentSourceVolume
            for Option in TransferOptionsTrackerInstance.GetObjectsAsList()
        ]
        DestinationLayoutItemInstances = [
            Option.DestinationLayoutItemInstance
            for Option in TransferOptionsTrackerInstance.GetObjectsAsList()
        ]
        DestinationPositions = [
            Option.DestinationPosition
            for Option in TransferOptionsTrackerInstance.GetObjectsAsList()
        ]
        CurrentDestinationVolumes = [
            Option.CurrentDestinationVolume
            for Option in TransferOptionsTrackerInstance.GetObjectsAsList()
        ]
        TransferVolumes = [
            Option.TransferVolume
            for Option in TransferOptionsTrackerInstance.GetObjectsAsList()
        ]

        MaxVolumes = [Volume - 0 for Volume in CurrentSourceVolumes]

        if (
            len(
                TestSumLessThanMax(
                    SourceLayoutItemInstances,
                    SourcePositions,
                    TransferVolumes,
                    MaxVolumes,
                )
            )
            != 0
        ):
            raise Exception(
                "There is not enough valume left in your source containers. TODO add more info"
            )
        # Does each source contain enough volume for this transfer?

        MaxVolumes = [Volume - 0 for Volume in CurrentDestinationVolumes]

        if (
            len(
                TestSumLessThanMax(
                    DestinationLayoutItemInstances,
                    DestinationPositions,
                    TransferVolumes,
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
                    SourceLayoutItemInstances,
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
                    DestinationLayoutItemInstances,
                )
            )
            != 0
        ):
            raise Exception(
                "This device does not support the labware of your destination layout item. TODO add more info"
            )
        # Are the source and destination items labware supported by this device?

        # Is the source and destintion in a correct pipetting deck location? TODO

        # NOTE: I played with sorting to make the liquid aspirate and dispense smarter. Trust me not a good idea. Try if you dare

        CommandTrackerInstance = CommandTracker()

        Counter = 0
        while Counter < TransferOptionsTrackerInstance.GetNumObjects():

            PickupOptionsTrackerInstance = PickupOptionsTracker()
            AspirateOptionsTrackerInstance = AspirateOptionsTracker()
            DispenseOptionsTrackerInstance = DispenseOptionsTracker()
            EjectOptionsTrackerInstance = EjectOptionsTracker()

            for PipettingChannel in self.ActiveChannels:

                TransferOptionsInstance = (
                    TransferOptionsTrackerInstance.GetObjectsAsList()[Counter]
                )

                SourceLayoutItemInstance = (
                    TransferOptionsInstance.SourceLayoutItemInstance
                )
                SourcePosition = TransferOptionsInstance.SourcePosition
                CurrentSourceVolume = TransferOptionsInstance.CurrentSourceVolume
                SourceMixCycles = TransferOptionsInstance.SourceMixCycles
                SourceLiquidClassCategory = (
                    TransferOptionsInstance.SourceLiquidClassCategory
                )
                DestinationLayoutItemInstance = (
                    TransferOptionsInstance.DestinationLayoutItemInstance
                )
                DestinationPosition = TransferOptionsInstance.DestinationPosition
                CurrentDestinationVolume = (
                    TransferOptionsInstance.CurrentDestinationVolume
                )
                DestinationMixCycles = TransferOptionsInstance.DestinationMixCycles
                DestinationLiquidClassCategory = (
                    TransferOptionsInstance.DestinationLiquidClassCategory
                )
                TransferVolume = TransferOptionsInstance.TransferVolume
                # Pull out our variables

                if Counter != (TransferOptionsTrackerInstance.GetNumObjects() - 1):
                    for Index in range(
                        Counter + 1, TransferOptionsTrackerInstance.GetNumObjects()
                    ):
                        if (
                            SourceLayoutItemInstance
                            == TransferOptionsTrackerInstance.GetObjectsAsList()[
                                Index
                            ].SourceLayoutItemInstance
                            and SourcePosition
                            == TransferOptionsTrackerInstance.GetObjectsAsList()[
                                Index
                            ].SourcePosition
                        ):
                            TransferOptionsTrackerInstance.GetObjectsAsList()[
                                Index
                            ].CurrentSourceVolume += (
                                CurrentSourceVolume + TransferVolume
                            )
                        # Source
                        if (
                            DestinationLayoutItemInstance
                            == TransferOptionsTrackerInstance.GetObjectsAsList()[
                                Index
                            ].DestinationLayoutItemInstance
                            and DestinationPosition
                            == TransferOptionsTrackerInstance.GetObjectsAsList()[
                                Index
                            ].DestinationPosition
                        ):
                            TransferOptionsTrackerInstance.GetObjectsAsList()[
                                Index
                            ].CurrentDestinationVolume += (
                                CurrentDestinationVolume + TransferVolume
                            )
                        # Destination
                    # Find the next same layoutitem and position then modify current volume

                SelectedPipetteTipInstance: None | PipetteTip = None
                for (
                    PipetteTipInstance
                ) in self.SupportedPipetteTipTrackerInstance.GetObjectsAsList():
                    if PipetteTipInstance.TipInstance.MaxVolume >= TransferVolume:
                        SelectedPipetteTipInstance = PipetteTipInstance
                        break
                # Get the tip we want to use
                if SelectedPipetteTipInstance is None:
                    SelectedPipetteTipInstance = (
                        self.SupportedPipetteTipTrackerInstance.GetObjectsAsList()[-1]
                    )
                # If we don't find a tip we are going to use the largest tip

                NumTransfers = ceil(
                    TransferVolume / SelectedPipetteTipInstance.TipInstance.MaxVolume
                )
                TransferVolume /= NumTransfers
                # Do we need to split this into mutliple transfers?

                if (
                    SelectedPipetteTipInstance.LiquidClassCategoryTrackerInstance.IsTracked(
                        SourceLiquidClassCategory
                    )
                    is True
                ):
                    SelectedSourceLiquidClassCategory = SelectedPipetteTipInstance.LiquidClassCategoryTrackerInstance.GetObjectByName(
                        SourceLiquidClassCategory
                    )
                else:
                    SelectedSourceLiquidClassCategory = SelectedPipetteTipInstance.LiquidClassCategoryTrackerInstance.GetObjectByName(
                        "Default"
                    )
                # Source
                if (
                    SelectedPipetteTipInstance.LiquidClassCategoryTrackerInstance.IsTracked(
                        DestinationLiquidClassCategory
                    )
                    is True
                ):
                    SelectedDestinationLiquidClassCategory = SelectedPipetteTipInstance.LiquidClassCategoryTrackerInstance.GetObjectByName(
                        DestinationLiquidClassCategory
                    )
                else:
                    SelectedDestinationLiquidClassCategory = SelectedPipetteTipInstance.LiquidClassCategoryTrackerInstance.GetObjectByName(
                        "Default"
                    )
                # Destination
                # Get the liqid class category we want to use

                for (
                    LiquidClassInstance
                ) in SelectedSourceLiquidClassCategory.GetObjectsAsList():
                    if LiquidClassInstance.MaxVolume >= TransferVolume:
                        SelectedSourceLiquidClass = LiquidClassInstance
                        break
                # Source
                for (
                    LiquidClassInstance
                ) in SelectedDestinationLiquidClassCategory.GetObjectsAsList():
                    if LiquidClassInstance.MaxVolume >= TransferVolume:
                        SelectedDestinationLiquidClass = LiquidClassInstance
                        break
                # Destination
                # Get the liquid class we want to use

                if CurrentDestinationVolume == 0:
                    DestinationMixCycles = 0
                # Do I need to modify the destination mixing cycles? If our current volume is zero then there is no reason to mix

                SourcePosition = (
                    ClampMax(
                        PipettingChannel,
                        SourceLayoutItemInstance.LabwareInstance.LabwareWells.SeqPerWell,  # type:ignore
                    )
                    + (
                        SourcePosition
                        * SourceLayoutItemInstance.LabwareInstance.LabwareWells.SeqPerWell  # type:ignore
                    )
                    - 1
                )
                # Clamp channel number into number of sequence positions for our source. Destination should, hopefully, always be a plate so clamping not needed

                DestinationPosition *= (
                    DestinationLayoutItemInstance.LabwareInstance.LabwareWells.SeqPerWell  # type: ignore
                )
                # Get correct destination position assuming any labware with any number of seq per well can be used

                PickupOptions(
                    "Pickup Tips Round 1",
                    SelectedPipetteTipInstance.TipInstance.PickupSequence,
                    PipettingChannel,
                    1,
                )
                # Create our PipettingOptions

                Counter += 1
                if Counter == TransferOptionsTrackerInstance.GetNumObjects():
                    break

        # Now the pipetting junk. aye yi yi
