from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools import Container
from PytomatedLiquidHandling.HAL import Labware, LayoutItem


@dataclass
class LoadedWell:
    LayoutItem: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    PhysicalWell: int
    ContainerWells: list[Container.Well.Well]


LoadedWells: list[LoadedWell] = list()


def QueueContainer(
    Container: Container.Container,
    Labware: Labware.Base.LabwareABC,
    RequireLid: bool = True,
    MeasureVolume: bool = False,
):
    ...


def ClearQueue():
    ...


def LoadQueue():
    ...


def UnloadQueue():
    ...


def GetLoadedWells(
    Well: Container.Well.Well,
) -> list[tuple[LayoutItem.CoverableItem | LayoutItem.NonCoverableItem, list[int]]]:
    ...


def GetLoadedLayoutItems(
    Container: Container.Container,
) -> list[LayoutItem.CoverableItem | LayoutItem.NonCoverableItem]:
    ...
