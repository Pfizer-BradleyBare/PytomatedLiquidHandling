from dataclasses import dataclass, field

from PytomatedLiquidHandling.API.Tools import Container


@dataclass
class NormalizeOptions(list):
    Source: Container.Well.Well
    Diluent: Container.Well.Well
    Destination: Container.Well.Well
    SourceConcentration: float
    TargetConcentration: float
    IntermediateWells: Container.Well.Well
    IntermediateConcentrations: None | list[float] = field(init=True, default=None)


def Normalize(Options: list[NormalizeOptions]):
    ...


def NormalizeTime(Options: list[NormalizeOptions]):
    ...