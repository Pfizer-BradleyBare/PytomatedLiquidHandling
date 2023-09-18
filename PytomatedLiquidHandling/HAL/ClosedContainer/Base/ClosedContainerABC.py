from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Callable, cast

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC


@dataclass
class ClosedContainerABC(InterfaceABC, HALObject):
    ToolSequence: str
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]
    SupportedLabwares: list[Labware.Base.LabwareABC]

    @dataclass(kw_only=True)
    class Options(OptionsABC):
        LayoutItem: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
        Position: int

    @abstractmethod
    def Open(self, Options: list[Options]):
        ...

    @abstractmethod
    def OpenTime(self, Options: list[Options]) -> float:
        ...

    @abstractmethod
    def Close(self, Options: list[Options]):
        ...

    @abstractmethod
    def CloseTime(self, Options: list[Options]) -> float:
        ...
