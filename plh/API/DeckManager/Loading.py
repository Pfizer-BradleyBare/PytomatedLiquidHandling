from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools import Container
from PytomatedLiquidHandling.HAL import Labware, LayoutItem


@dataclass
class LoadedWell:
    ContainerWell: Container.Well.Well
    LayoutItem: LayoutItem.CoverablePlate | LayoutItem.Plate
    LayoutItemWell: int


LoadedWells: list[LoadedWell] = list()


def QueueContainer(
    Container: Container.Container,
    Labware: Labware.Base.LabwareABC,
    RequireLid: bool = True,
    MeasureVolume: bool = False,
    Disposable: bool = False,
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
) -> list[tuple[LayoutItem.CoverablePlate | LayoutItem.Plate, list[int]]]:
    ...


def GetLoadedLayoutItems(
    Container: Container.Container,
) -> list[LayoutItem.CoverablePlate | LayoutItem.Plate]:
    ...