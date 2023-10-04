from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools import Container
from PytomatedLiquidHandling.HAL import DeckLoaders, Labware, LayoutItem


@dataclass
class LoadedWell:
    LayoutItem: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    PhysicalWell: int
    ContainerWells: list[Container.Well.Well]


LoadedWells: list[LoadedWell] = list()


def LoadContainer(
    Container: Container.Container,
    Labware: Labware.Base.LabwareABC,
    RequireLid: bool = True,
    MeasureVolume: bool = False,
):
    ...


def UnloadContainer(Container: Container.Container):
    ...


def GetLoadedWells(
    Well: Container.Well.Well,
) -> list[tuple[LayoutItem.CoverableItem | LayoutItem.NonCoverableItem, list[int]]]:
    ...
