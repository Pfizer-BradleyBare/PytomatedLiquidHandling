from dataclasses import dataclass

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.API.ExecutionEngine.Orchastrator.LoadedLayoutItem import (
    LoadedLayoutItem,
)
from PytomatedLiquidHandling.HAL import LayoutItem


@dataclass
class Options(OptionsABC):
    LoadedLayoutItemInstance: LoadedLayoutItem
    DestinationLayoutItem: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
