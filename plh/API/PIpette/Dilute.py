from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools import Container


@dataclass
class DiluteOptions:
    Source: Container.Well.Well
    Diluent: Container.Well.Well
    Destination: Container.Well.Well
    SourceConcentration: float
    TargetConcentration: float


def Dilute(Options: list[DiluteOptions]):
    ...


def DiluteTime(Options: list[DiluteOptions]):
    ...
