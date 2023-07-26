from dataclasses import dataclass, field
from abc import abstractmethod

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import (
    OptionsABC,
    OptionsTrackerABC,
)
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC

from ...Tools.AbstractClasses import InterfaceABC, OptionsTrackerInterfaceCommandABC


@dataclass(frozen=True)
class ClosedContainerInterfaceCommand(
    OptionsTrackerInterfaceCommandABC[
        None, "ClosedContainerInterfaceCommand.OptionsTracker"  # type:ignore
    ]
):
    @dataclass(kw_only=True)
    class Options(OptionsABC):
        LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
        Position: int

    @dataclass
    class OptionsTracker(OptionsTrackerABC[Options]):
        ...


@dataclass
class ClosedContainerABC(InterfaceABC, UniqueObjectABC):
    ToolSequence: str
    SupportedDeckLocationTrackerInstance: DeckLocation.DeckLocationTracker
    SupportedLabwareTrackerInstance: Labware.LabwareTracker
    Open: ClosedContainerInterfaceCommand = field(init=False)
    Close: ClosedContainerInterfaceCommand = field(init=False)

    @abstractmethod
    def _Open(
        self, OptionsTrackerInstance: ClosedContainerInterfaceCommand.OptionsTracker
    ):
        ...

    @abstractmethod
    def _OpenTime(
        self, OptionsTrackerInstance: ClosedContainerInterfaceCommand.OptionsTracker
    ) -> float:
        ...

    @abstractmethod
    def _Close(
        self, OptionsTrackerInstance: ClosedContainerInterfaceCommand.OptionsTracker
    ):
        ...

    @abstractmethod
    def _CloseTime(
        self, OptionsTrackerInstance: ClosedContainerInterfaceCommand.OptionsTracker
    ) -> float:
        ...

    def __post_init__(self):
        InterfaceABC.__post_init__(self)
        self.Open = ClosedContainerInterfaceCommand(
            Execute=self._Open, ExecutionTime=self._OpenTime
        )
        self.Close = ClosedContainerInterfaceCommand(
            Execute=self._Close, ExecutionTime=self._CloseTime
        )
