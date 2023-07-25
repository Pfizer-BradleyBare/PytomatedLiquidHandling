from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import (
    OptionsABC,
    OptionsTrackerABC,
)
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Tools.AbstractClasses import InterfaceABC
from .Interface import OpenCloseOptions


class OptionsTrackerInterfaceABC(ABC):
    @abstractmethod
    def Execute(self, OptionsTrackerInstance: OptionsTrackerABC):
        ...

    @abstractmethod
    def ExecutionTime(self, OptionsTrackerInstance: OptionsTrackerABC):
        ...


class OpenInterfaceABC(ABC):
    @dataclass(kw_only=True)
    class Options(OptionsABC):
        LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
        Position: int

    @dataclass
    class OptionsTracker(OptionsTrackerABC[Options]):
        ...

    @abstractmethod
    def Execute(self, OptionsTrackerInstance: OptionsTracker):
        ...

    @abstractmethod
    def ExecutionTime(self, OptionsTrackerInstance: OptionsTracker):
        ...


@dataclass
class ClosedContainerABC(InterfaceABC, UniqueObjectABC):
    ToolSequence: str
    SupportedDeckLocationTrackerInstance: DeckLocation.DeckLocationTracker
    SupportedLabwareTrackerInstance: Labware.LabwareTracker

    @abstractmethod
    def Open(self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker):
        ...

    @abstractmethod
    def Close(
        self, *, OpenCloseOptionsTrackerInstance: OpenCloseOptions.OptionsTracker
    ):
        ...
