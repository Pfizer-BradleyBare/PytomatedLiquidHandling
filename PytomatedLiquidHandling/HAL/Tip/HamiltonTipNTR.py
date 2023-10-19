from dataclasses import dataclass, field
from typing import cast

from ...Driver.Hamilton.Backend.BaseHamiltonBackend import HamiltonBackendABC
from ...Driver.Hamilton.Tip import Visual_NTR_Library
from .Base import TipABC


@dataclass
class HamiltonTipNTR(TipABC):
    Backend: HamiltonBackendABC
    NumTiers: int
    TipsPerRack: int
    RackWasteLabwareID: str
    GripperLabwareID: str
    TierDiscardNumber: int = field(init=False, default=100)
    DiscardedRackLabwareIDs: list[str] = field(init=False, default_factory=list)

    def RemainingTipsInTier(self) -> int:
        Remaining = self.RemainingTips() % (self.TipsPerRack * self.NumTiers)

        if Remaining == 0:
            AvailableIDs = set([Pos.LabwareID for Pos in self.AvailablePositions])

            if len(AvailableIDs) + len(self.DiscardedRackLabwareIDs) == len(
                self.RackLabwareIDs
            ):
                return self.TipsPerRack * self.NumTiers
                # We are at the start of a fresh layer
            else:
                return 0
                # We just emptied a layer and must discard

        return Remaining

    def DiscardTierLayerToWaste(self):
        PresentLabwareIDs = list(
            set([Pos.LabwareID for Pos in self.AvailablePositions])
        )
        DiscardLabwareIDs = [
            RackID
            for RackID in self.RackLabwareIDs
            if RackID not in PresentLabwareIDs
            and RackID not in self.DiscardedRackLabwareIDs
        ]

        for i in range(0, self.TierDiscardNumber - len(DiscardLabwareIDs)):
            DiscardLabwareIDs.append(PresentLabwareIDs[i])
        # Basically we should always discard the same number of racks as we have tiers.
        # There is a special case during tip counter edit where an NTR rack is removed manually by the user. We handle that here.

        for DiscardLabwareID in DiscardLabwareIDs:
            self.DiscardedRackLabwareIDs.append(DiscardLabwareID)
            ...
            # TODO: Do the discard with CORE grippers here

        self.AvailablePositions = [
            Pos
            for Pos in self.AvailablePositions
            if Pos.LabwareID not in self.DiscardedRackLabwareIDs
        ]
        # Update available positions

        self.TierDiscardNumber = self.NumTiers
        # Reset the Tier discard number. This will only be changed here and in the TipCounterEdit method

        if len(self.AvailablePositions) == 0:
            Command = Visual_NTR_Library.Channels_TipCounter_Write.Command(
                ListedOptions=Visual_NTR_Library.Channels_TipCounter_Write.ListedOptions(
                    TipCounter="HamiltonTipNTR_" + str(self.MaxVolume) + "uL_TipCounter"
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.Backend.ExecuteCommand(Command)
            self.Backend.WaitForResponseBlocking(Command)
            self.Backend.GetResponse(
                Command, Visual_NTR_Library.Channels_TipCounter_Write.Response
            )
            self.TipCounterEdit()

    def TipCounterEdit(self):
        ListedOptions = Visual_NTR_Library.Channels_TipCounter_Edit.ListedOptions(
            TipCounter="HamiltonTipNTR_" + str(self.MaxVolume) + "uL_TipCounter",
            DialogTitle="Please update the number of "
            + str(self.MaxVolume)
            + "uL tips currently loaded on the system",
        )
        for ID in self.RackLabwareIDs:
            ListedOptions.append(
                Visual_NTR_Library.Channels_TipCounter_Edit.Options(ID)
            )

        CommandInstance = Visual_NTR_Library.Channels_TipCounter_Edit.Command(
            ListedOptions=ListedOptions,
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

        AvailableIDs = set([Pos.LabwareID for Pos in self.AvailablePositions])
        self.DiscardedRackLabwareIDs = [
            ID for ID in self.RackLabwareIDs if ID not in AvailableIDs
        ]
        # We automatically assume the if a labwareID is NOT in the available positions, then it is basically already discarded.

        self.TierDiscardNumber = len(self.DiscardedRackLabwareIDs) % self.NumTiers
        # Once we know which labwareIDs are already gone we can calculate how many to throw away on the first pass.
        # We basically say: "I assume to have a multiple of NumTiers so if I have any remainder then that is number of tiers to be thrown away."
