from dataclasses import dataclass, field


from PytomatedLiquidHandling.API import DeckManager
from PytomatedLiquidHandling.API.Tools import Container
from PytomatedLiquidHandling.HAL import PipetteDevices, ClosedContainerDevices


@dataclass
class DiluteOptions:
    ...


def Dilute():
    ...


def DiluteTime():
    ...
