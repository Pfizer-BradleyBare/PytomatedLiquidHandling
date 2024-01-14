from dataclasses import field
from typing import Literal, cast

from pydantic import dataclasses
from PytomatedLiquidHandling.Driver.Hamilton import Backend, Visual_NTR_Library
from PytomatedLiquidHandling.HAL import DeckLocation, LayoutItem

from .Base import TipABC


@dataclasses.dataclass(kw_only=True)
class HamiltonNTR(TipABC):
    Backend: Backend.HamiltonBackendABC
    BackendErrorHandling: Literal["N/A"] = "N/A"

    Tiers: int
    TipRackWaste: LayoutItem.TipRack
    _TierDiscardNumber: int = field(init=False, default=100)
    _DiscardedTipRacks: list[LayoutItem.TipRack] = field(
        init=False,
        default_factory=list,
    )

    def RemainingTipsInTier(self) -> int:
        Remaining = self.RemainingTips() % (self.TipsPerRack * self.Tiers)

        if Remaining == 0:
            AvailableIDs = set([Pos.LabwareID for Pos in self._AvailablePositions])

            if len(AvailableIDs) + len(self._DiscardedTipRacks) == len(self.TipRacks):
                return self.TipsPerRack * self.Tiers
                # We are at the start of a fresh layer
            else:
                return 0
                # We just emptied a layer and must discard

        return Remaining

    def DiscardLayerToWaste(self):
        PresentLabwareIDs = list(
            set([Pos.LabwareID for Pos in self._AvailablePositions]),
        )
        PresentTipRacks = [
            TipRack
            for TipRack in self.TipRacks
            if TipRack.LabwareID not in PresentLabwareIDs
        ]
        DiscardTipRacks = [
            TipRack
            for TipRack in self.TipRacks
            if TipRack.LabwareID not in PresentLabwareIDs
            and TipRack not in self._DiscardedTipRacks
        ]

        for i in range(self._TierDiscardNumber - len(DiscardTipRacks)):
            DiscardTipRacks.append(PresentTipRacks[i])
        # Basically we should always discard the same number of racks as we have tiers.
        # There is a special case during tip counter edit where an NTR rack is removed manually by the user. We handle that here.

        for TipRack in DiscardTipRacks:
            self._DiscardedTipRacks.append(TipRack)
            DeckLocation.TransportableDeckLocation.GetCompatibleTransportConfigs(
                TipRack.DeckLocation,
                self.TipRackWaste.DeckLocation,
            )[0][0].TransportDevice.Transport(TipRack, self.TipRackWaste)

        self._AvailablePositions = [
            Pos
            for Pos in self._AvailablePositions
            if Pos.LabwareID
            not in [TipRack.LabwareID for TipRack in self._DiscardedTipRacks]
        ]
        # Update available positions

        self._TierDiscardNumber = self.Tiers
        # Reset the Tier discard number. This will only be changed here and in the TipCounterEdit method

        if len(self._AvailablePositions) == 0:
            raise RuntimeError("Out of tips. Reload tips.")

    def UpdateAvailablePositions(self):
        CommandInstance = Visual_NTR_Library.Channels_TipCounter_Edit.Command(
            Options=Visual_NTR_Library.Channels_TipCounter_Edit.OptionsList(
                TipCounter="HamiltonTipNTR_" + str(self.Volume) + "uL_TipCounter",
                DialogTitle="Please update the number of "
                + str(self.Volume)
                + "uL tips currently loaded on the system",
            ),
        )
        for TipRack in self.TipRacks:
            CommandInstance.Options.append(
                Visual_NTR_Library.Channels_TipCounter_Edit.Options(
                    LabwareID=TipRack.LabwareID,
                ),
            )

        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self._ParseAvailablePositions(
            cast(
                list[dict[str, str]],
                self.Backend.GetResponse(
                    CommandInstance,
                    Visual_NTR_Library.Channels_TipCounter_Edit.Response,
                ).AvailablePositions,
            ),
        )

        AvailableIDs = set([Pos.LabwareID for Pos in self._AvailablePositions])
        self._DiscardedTipRacks = [
            TipRack
            for TipRack in self.TipRacks
            if TipRack.LabwareID not in AvailableIDs
        ]
        # We automatically assume the if a labwareID is NOT in the available positions, then it is basically already discarded.

        self._TierDiscardNumber = len(self._DiscardedTipRacks) % self.Tiers
        # Once we know which labwareIDs are already gone we can calculate how many to throw away on the first pass.
        # We basically say: "I assume to have a multiple of NumTiers so if I have any remainder then that is number of tiers to be thrown away."
