from copy import copy
from typing import cast

from pydantic import BaseModel, PrivateAttr

from PytomatedLiquidHandling.Driver.Hamilton import (
    Backend,
    EntryExit,
    HSLTipCountingLib,
)

from .Base import TipABC


class HamiltonEENTR(TipABC):
    class TipStack(BaseModel):
        LabwareID: str
        ModuleNumber: int
        StackNumber: int
        _StackCount: int = PrivateAttr(default=0)

    Backend: Backend.HamiltonBackendABC

    TipStacks: list[TipStack]
    RacksPerStack: int
    TipRackWasteLabwareID: str

    def Initialize(self):
        TipABC.Initialize(self)

    def RemainingTips(self) -> int:
        return self.RemainingTipsInTier() + sum(
            [self.TipsPerRack * Stack._StackCount for Stack in self.TipStacks]
        )

    def RemainingTipsInTier(self) -> int:
        return TipABC.RemainingTips(self)

    def DiscardLayerToWaste(self):
        for Rack in self.TipRacks:
            for Stack in self.TipStacks:
                if Stack._StackCount == 0:
                    continue
                # only use stacks that have racks

                CommandInstance = EntryExit.MoveToBeam.Command(
                    Options=EntryExit.MoveToBeam.Options(
                        ModuleNumber=Stack.ModuleNumber,
                        StackNumber=Stack.StackNumber,
                        OffsetFromBeam=0,
                    ),
                    CustomErrorHandling=self.CustomErrorHandling,
                )

                self.Backend.ExecuteCommand(CommandInstance)
                self.Backend.WaitForResponseBlocking(CommandInstance)
                self.Backend.GetResponse(CommandInstance, EntryExit.MoveToBeam.Response)
                # Move the stack to beam so we can access the tip rack.

                Stack._StackCount -= 1

                TipRackWasteLayoutItem = copy(Rack)
                TipRackWasteLayoutItem.LabwareID = self.TipRackWasteLabwareID
                # Use the tip rack layout item to make the waste layout item

                TransportDevice = Rack.DeckLocation.TransportConfig.TransportDevice
                TransportDevice.Transport(Rack, TipRackWasteLayoutItem)
                # Dispose of the empty rack

                StackTipRackLayoutItem = copy(Rack)
                StackTipRackLayoutItem.LabwareID = Stack.LabwareID
                # Use the tip rack layout item to make the Tip Rack Stack layout item

                TransportDevice = Rack.DeckLocation.TransportConfig.TransportDevice
                TransportDevice.Transport(Rack, StackTipRackLayoutItem)
                # Move the full rack from the stack.

    def UpdateAvailablePositions(self):
        for Stack in self.TipStacks:
            CommandInstance = EntryExit.CountLabwareInStack.Command(
                Options=EntryExit.CountLabwareInStack.Options(
                    ModuleNumber=Stack.ModuleNumber,
                    StackNumber=Stack.StackNumber,
                    LabwareID=Stack.LabwareID,
                    IsNTRRack=True,
                ),
                CustomErrorHandling=self.CustomErrorHandling,
            )
            self.Backend.ExecuteCommand(CommandInstance)
            self.Backend.WaitForResponseBlocking(CommandInstance)
            Stack._StackCount = self.Backend.GetResponse(
                CommandInstance, EntryExit.CountLabwareInStack.Response
            ).NumLabware

        CommandInstance = HSLTipCountingLib.Edit.Command(
            Options=HSLTipCountingLib.Edit.ListedOptions(
                TipCounter="HamiltonTipFTR_" + str(self.Volume) + "uL_TipCounter",
                DialogTitle="Please update the number of "
                + str(self.Volume)
                + "uL tips currently loaded on the system",
            )
        )
        for TipRack in self.TipRacks:
            CommandInstance.Options.append(
                HSLTipCountingLib.Edit.Options(LabwareID=TipRack.LabwareID)
            )

        self.Backend.ExecuteCommand(CommandInstance)
        self.Backend.WaitForResponseBlocking(CommandInstance)
        self._ParseAvailablePositions(
            cast(
                list[dict[str, str]],
                self.Backend.GetResponse(
                    CommandInstance, HSLTipCountingLib.Edit.Response
                ).AvailablePositions,
            )
        )
