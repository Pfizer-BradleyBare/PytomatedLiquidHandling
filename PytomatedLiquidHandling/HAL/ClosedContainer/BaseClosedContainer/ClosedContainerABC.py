from abc import ABC, abstractmethod
from dataclasses import dataclass


from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import (
    OptionsABC,
    OptionsTrackerABC,
)
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Tools.AbstractClasses import InterfaceABC, OptionsTrackerInterfaceCommandABC


@dataclass(kw_only=True)
class OpenCloseOptions(OptionsABC):
    LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
    Position: int


@dataclass
class ClosedContainerABC(InterfaceABC, UniqueObjectABC):
    ToolSequence: str
    SupportedDeckLocationTrackerInstance: DeckLocation.DeckLocationTracker
    SupportedLabwareTrackerInstance: Labware.LabwareTracker

    class OpenCommand(OptionsTrackerInterfaceCommandABC):
        @dataclass(kw_only=True)
        class Options(OpenCloseOptions):
            ...

        @dataclass
        class OptionsTracker(OptionsTrackerABC[Options]):
            ...

    class CloseCommand(OptionsTrackerInterfaceCommandABC):
        @dataclass(kw_only=True)
        class Options(OpenCloseOptions):
            ...

        @dataclass
        class OptionsTracker(OptionsTrackerABC[Options]):
            ...
