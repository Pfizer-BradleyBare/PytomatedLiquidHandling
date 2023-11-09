from typing import cast

from pydantic import PrivateAttr, field_validator

from PytomatedLiquidHandling.HAL import LayoutItem, TransportDevice

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Tip import Visual_NTR_Library
from .Base import TipABC


class HamiltonNTR(TipABC):
    Tiers: int
    TipsPerRack: int
    TipRackWaste: LayoutItem.TipRack
    TransportDevice: TransportDevice.Base.TransportDeviceABC
    _TierDiscardNumber: int = PrivateAttr(default=100)
    _DiscardedRackLabwareIDs: list[str] = PrivateAttr(default_factory=list)

    @field_validator("TipRackWaste", mode="before")
    def __TipRackWasteValidate(cls, v):
        Objects = LayoutItem.Devices

        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + LayoutItem.Base.LayoutItemABC.__name__
                + " objects."
            )

        return Objects[Identifier]

    @field_validator("TransportDevice", mode="before")
    def __TransportDeviceValidate(cls, v):
        Objects = TransportDevice.Devices

        Identifier = v

        if Identifier not in Objects:
            raise ValueError(
                Identifier
                + " is not found in "
                + TransportDevice.Base.TransportDeviceABC.__name__
                + " objects."
            )

        return Objects[Identifier]

    def RemainingTipsInTier(self) -> int:
        Remaining = self.RemainingTips() % (self.TipsPerRack * self.Tiers)

        if Remaining == 0:
            AvailableIDs = set([Pos.LabwareID for Pos in self._AvailablePositions])

            if len(AvailableIDs) + len(self._DiscardedRackLabwareIDs) == len(
                self.RackLabwareIDs
            ):
                return self.TipsPerRack * self.Tiers
                # We are at the start of a fresh layer
            else:
                return 0
                # We just emptied a layer and must discard

        return Remaining

    def DiscardTierLayerToWaste(self):
        PresentLabwareIDs = list(
            set([Pos.LabwareID for Pos in self._AvailablePositions])
        )
        DiscardLabwareIDs = [
            RackID
            for RackID in self.RackLabwareIDs
            if RackID not in PresentLabwareIDs
            and RackID not in self._DiscardedRackLabwareIDs
        ]

        for i in range(0, self._TierDiscardNumber - len(DiscardLabwareIDs)):
            DiscardLabwareIDs.append(PresentLabwareIDs[i])
        # Basically we should always discard the same number of racks as we have tiers.
        # There is a special case during tip counter edit where an NTR rack is removed manually by the user. We handle that here.

        for DiscardLabwareID in DiscardLabwareIDs:
            self._DiscardedRackLabwareIDs.append(DiscardLabwareID)
            ...
            # TODO: Do the discard with CORE grippers here

        self._AvailablePositions = [
            Pos
            for Pos in self._AvailablePositions
            if Pos.LabwareID not in self._DiscardedRackLabwareIDs
        ]
        # Update available positions

        self._TierDiscardNumber = self.Tiers
        # Reset the Tier discard number. This will only be changed here and in the TipCounterEdit method

        if len(self._AvailablePositions) == 0:
            Command = Visual_NTR_Library.Channels_TipCounter_Write.Command(
                Options=Visual_NTR_Library.Channels_TipCounter_Write.ListedOptions(
                    TipCounter="HamiltonTipNTR_" + str(self.Volume) + "uL_TipCounter"
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.Backend.ExecuteCommand(Command)
            self.Backend.WaitForResponseBlocking(Command)
            self.Backend.GetResponse(
                Command, Visual_NTR_Library.Channels_TipCounter_Write.Response
            )
            self.TipCounterEdit()

        # TODO. Need to move the racks to waste with a transport device...

    def TipCounterEdit(self):
        ListedOptions = Visual_NTR_Library.Channels_TipCounter_Edit.ListedOptions(
            TipCounter="HamiltonTipNTR_" + str(self.Volume) + "uL_TipCounter",
            DialogTitle="Please update the number of "
            + str(self.Volume)
            + "uL tips currently loaded on the system",
        )
        for ID in self.RackLabwareIDs:
            ListedOptions.append(
                Visual_NTR_Library.Channels_TipCounter_Edit.Options(ID)
            )

        CommandInstance = Visual_NTR_Library.Channels_TipCounter_Edit.Command(
            Options=ListedOptions,
            CustomErrorHandling=self.CustomErrorHandling,
        )
        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self._ParseAvailablePositions(
            cast(
                list[dict[str, str]],
                self.Backend.GetResponse(
                    CommandInstance,
                    Visual_NTR_Library.Channels_TipCounter_Edit.Response,
                ).GetAvailablePositions(),
            )
        )

        AvailableIDs = set([Pos.LabwareID for Pos in self._AvailablePositions])
        self._DiscardedRackLabwareIDs = [
            ID for ID in self.RackLabwareIDs if ID not in AvailableIDs
        ]
        # We automatically assume the if a labwareID is NOT in the available positions, then it is basically already discarded.

        self._TierDiscardNumber = len(self._DiscardedRackLabwareIDs) % self.Tiers
        # Once we know which labwareIDs are already gone we can calculate how many to throw away on the first pass.
        # We basically say: "I assume to have a multiple of NumTiers so if I have any remainder then that is number of tiers to be thrown away."
