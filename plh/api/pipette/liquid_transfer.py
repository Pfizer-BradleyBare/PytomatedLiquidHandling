from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools import Container


@dataclass
class LiquidTransferOptions:
    Source: Container.Well.Well
    Destination: Container.Well.Well
    Volume: float


def LiquidTransfer(Options: list[LiquidTransferOptions]):
    ...


def LiquidTransferTime(Options: list[LiquidTransferOptions]):
    ...
