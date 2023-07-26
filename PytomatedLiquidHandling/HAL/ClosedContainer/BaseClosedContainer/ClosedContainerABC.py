from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Callable, cast

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import (
    OptionsABC,
    OptionsTrackerABC,
)
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Tools.AbstractClasses import InterfaceABC, OptionsTrackerInterfaceCommandABC


@dataclass
class ClosedContainerABC(InterfaceABC, UniqueObjectABC):
    class OpenCloseInterfaceCommand(OptionsTrackerInterfaceCommandABC[None]):
        @dataclass(kw_only=True)
        class Options(OptionsABC):
            LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
            Position: int

        @dataclass
        class OptionsTracker(OptionsTrackerABC[Options]):
            ...

    ToolSequence: str
    SupportedDeckLocationTrackerInstance: DeckLocation.DeckLocationTracker
    SupportedLabwareTrackerInstance: Labware.LabwareTracker
    Open: OpenCloseInterfaceCommand = field(init=False)
    Close: OpenCloseInterfaceCommand = field(init=False)

    @abstractmethod
    def _Open(self, OptionsTrackerInstance: OpenCloseInterfaceCommand.OptionsTracker):
        ...

    @abstractmethod
    def _OpenTime(
        self, OptionsTrackerInstance: OpenCloseInterfaceCommand.OptionsTracker
    ) -> float:
        ...

    @abstractmethod
    def _Close(self, OptionsTrackerInstance: OpenCloseInterfaceCommand.OptionsTracker):
        ...

    @abstractmethod
    def _CloseTime(
        self, OptionsTrackerInstance: OpenCloseInterfaceCommand.OptionsTracker
    ) -> float:
        ...

    def __post_init__(self):
        InterfaceABC.__post_init__(self)
        self.Open = ClosedContainerABC.OpenCloseInterfaceCommand(
            ExecuteFunction=self._Open,
            ExecutionTimeFunction=self._OpenTime,
        )
        self.Close = ClosedContainerABC.OpenCloseInterfaceCommand(
            ExecuteFunction=self._Close,
            ExecutionTimeFunction=self._CloseTime,
        )
