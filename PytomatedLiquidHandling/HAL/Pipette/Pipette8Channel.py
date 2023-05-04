from math import ceil

from ...Driver.Pipette import SingleChannel as Pipette8ChannelDriver
from ..Labware import Labware, LabwareTracker
from ..Pipette import TransferOptions, TransferOptionsTracker
from .BasePipette import Pipette, PipetteTipTracker, PipettingDeviceTypes
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

    def Initialize(
        self,
    ):
        ...

    def Deinitialize(
        self,
    ):
        ...

    def LabwaresSupported(
        self,
        LabwareInstances: list[Labware],
    ) -> bool:
        ...

    def Transfer(
        self,
        TransferOptionsTrackerInstance: TransferOptionsTracker,
    ):
        # NOTE: I played with sorting to make the liquid aspirate and dispense smarter. Trust me not a good idea. Try if you dare

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

        TipTransferCategories: dict[str, list[TransferOptions]] = dict()
        for (
            PipetteTipInstance
        ) in self.SupportedPipetteTipTrackerInstance.GetObjectsAsList():
            TipTransferCategories[PipetteTipInstance.GetUniqueIdentifier()] = list()

        for (
            TransferOptionsInstance
        ) in TransferOptionsTrackerInstance.GetObjectsAsList():
            for Key in TipTransferCategories:
                PipetteTipInstance = (
                    self.SupportedPipetteTipTrackerInstance.GetObjectByName(Key)
                )
                if (
                    PipetteTipInstance.TipInstance.MaxVolume
                    >= TransferOptionsInstance.TransferVolume
                ):
                    TipTransferCategories[Key].append(TransferOptionsInstance)
                    break

                if Key == list(TipTransferCategories.keys())[-1]:
                    NumTransfers = ceil(
                        TransferOptionsInstance.TransferVolume
                        / PipetteTipInstance.TipInstance.MaxVolume
                    )
                    TransferOptionsInstance.NumTransfers = NumTransfers
                    TransferOptionsInstance.TransferVolume /= NumTransfers

                    for i in range(0, NumTransfers):
                        TipTransferCategories[Key].append(TransferOptionsInstance)

                    break
                # Our transfer volume is larger than our biggest tip. Let's deal with that
        # lets categorize our transfer into tip "buckets"

        for Key in TipTransferCategories:
            PipetteTipInstance = (
                self.SupportedPipetteTipTrackerInstance.GetObjectByName(Key)
            )

            TransferOptionsInstances = TipTransferCategories[Key]

            NumTransferOptions = len(TransferOptionsInstances)
            NumActiveChannels = len(self.ActiveChannels)
            Counter = 0

            while Counter < NumTransferOptions:
                PickupOptionsTrackerInstance = (
                    Pipette8ChannelDriver.Pickup.OptionsTracker()
                )
                AspirateOptionsTrackerInstance = (
                    Pipette8ChannelDriver.Aspirate.OptionsTracker()
                )
                DispenseOptionsTrackerInstance = (
                    Pipette8ChannelDriver.Dispense.OptionsTracker()
                )
                EjectOptionsTrackerInstance = (
                    Pipette8ChannelDriver.Eject.OptionsTracker()
                )

                if NumTransferOptions - Counter >= NumActiveChannels:
                    NumRequiredTips = NumActiveChannels
                else:
                    NumRequiredTips = NumTransferOptions - Counter

                PipetteTipInstance.TipInstance.UpdateTipPosition(NumRequiredTips)
                CurrentTipPosition = (
                    PipetteTipInstance.TipInstance.GetCurrentTipPosition()
                )
                # Update the tip position and get it.

                for PipettingChannel in self.ActiveChannels:
                    TransferOptionsInstance = TransferOptionsInstances[Counter]

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
                                ].CurrentSourceVolume = (
                                    CurrentSourceVolume
                                    - TransferVolume
                                    # We remove liquid from source
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
                                ].CurrentDestinationVolume = (
                                    CurrentDestinationVolume
                                    + TransferVolume
                                    # We add liquid to destination
                                )
                            # Destination
                        # Find the next same layoutitem and position then modify current volume

                    if (
                        PipetteTipInstance.LiquidClassCategoryTrackerInstance.IsTracked(
                            SourceLiquidClassCategory
                        )
                        is True
                    ):
                        SelectedSourceLiquidClassCategory = PipetteTipInstance.LiquidClassCategoryTrackerInstance.GetObjectByName(
                            SourceLiquidClassCategory
                        )
                    else:
                        SelectedSourceLiquidClassCategory = PipetteTipInstance.LiquidClassCategoryTrackerInstance.GetObjectByName(
                            "Default"
                        )
                    # Source
                    if (
                        PipetteTipInstance.LiquidClassCategoryTrackerInstance.IsTracked(
                            DestinationLiquidClassCategory
                        )
                        is True
                    ):
                        SelectedDestinationLiquidClassCategory = PipetteTipInstance.LiquidClassCategoryTrackerInstance.GetObjectByName(
                            DestinationLiquidClassCategory
                        )
                    else:
                        SelectedDestinationLiquidClassCategory = PipetteTipInstance.LiquidClassCategoryTrackerInstance.GetObjectByName(
                            "Default"
                        )
                    # Destination
                    # Get the liqid class category we want to use

                    SelectedSourceLiquidClass = (
                        SelectedSourceLiquidClassCategory.GetObjectsAsList()[-1]
                    )
                    for (
                        LiquidClassInstance
                    ) in SelectedSourceLiquidClassCategory.GetObjectsAsList():
                        if LiquidClassInstance.MaxVolume >= TransferVolume:
                            SelectedSourceLiquidClass = LiquidClassInstance
                            break
                    # Source
                    SelectedDestinationLiquidClass = (
                        SelectedDestinationLiquidClassCategory.GetObjectsAsList()[-1]
                    )
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

                    PickupOptionsTrackerInstance.LoadSingle(
                        Pipette8ChannelDriver.Pickup.Options(
                            PipetteTipInstance.TipInstance.PickupSequence,
                            PipettingChannel,
                            CurrentTipPosition,
                        )
                    )
                    CurrentTipPosition += 1
                    # Pickup

                    AspirateOptionsInstance = Pipette8ChannelDriver.Aspirate.Options(
                        PipettingChannel,
                        SourceLayoutItemInstance.Sequence,
                        SourcePosition,
                        SelectedSourceLiquidClass.GetUniqueIdentifier(),
                        TransferVolume,
                    )
                    # TODO Configure Options Further
                    AspirateOptionsTrackerInstance.LoadSingle(AspirateOptionsInstance)
                    # Aspirate

                    DispenseOptionsInstance = Pipette8ChannelDriver.Dispense.Options(
                        PipettingChannel,
                        SourceLayoutItemInstance.Sequence,
                        SourcePosition,
                        SelectedDestinationLiquidClass.GetUniqueIdentifier(),
                        TransferVolume,
                    )
                    # TODO Configure Options Further
                    DispenseOptionsTrackerInstance.LoadSingle(DispenseOptionsInstance)
                    # Dispense

                    EjectOptionsTrackerInstance.LoadSingle(
                        Pipette8ChannelDriver.Eject.Options(
                            PipetteTipInstance.WasteSequence,
                            PipettingChannel,
                            PipettingChannel,
                        )
                    )
                    # Eject
                    # Create our PipettingOptions

                    Counter += 1
                    if Counter == TransferOptionsTrackerInstance.GetNumObjects():
                        break

                try:
                    Pipette8ChannelDriver.Pickup.Command(
                        PickupOptionsTrackerInstance, True
                    ).Execute()
                except:
                    ...

                try:
                    Pipette8ChannelDriver.Aspirate.Command(
                        AspirateOptionsTrackerInstance, True
                    )
                except:
                    ...

                try:
                    Pipette8ChannelDriver.Dispense.Command(
                        DispenseOptionsTrackerInstance, True
                    )
                except:
                    ...

                try:
                    Pipette8ChannelDriver.Eject.Command(
                        EjectOptionsTrackerInstance, True
                    )
                except:
                    ...
                # Lets assume this is perfect and will not need error handling yet
