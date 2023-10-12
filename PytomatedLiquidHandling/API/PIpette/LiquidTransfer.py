from dataclasses import dataclass


from PytomatedLiquidHandling.API import DeckManager
from PytomatedLiquidHandling.API.Tools import Container
from PytomatedLiquidHandling.HAL import PipetteDevices, ClosedContainerDevices


@dataclass
class LiquidTransferOptions:
    Source: Container.Well.Well
    Destination: Container.Well.Well
    Volume: float


def LiquidTransfer(Options: list[LiquidTransferOptions]):
    ...


def LiquidTransferTime(Options: list[LiquidTransferOptions]):
    ...
