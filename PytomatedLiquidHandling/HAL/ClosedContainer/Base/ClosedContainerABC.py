from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Callable, cast

from PytomatedLiquidHandling.Driver.Tools.AbstractClasses import OptionsABC
from PytomatedLiquidHandling.HAL import DeckLocation, Labware, LayoutItem
from PytomatedLiquidHandling.HAL.Tools.AbstractClasses import HALObject

from ...Tools.AbstractClasses import InterfaceABC, InterfaceCommandWithListedOptionsABC


@dataclass
class ClosedContainerABC(InterfaceABC, HALObject):
    class OpenCloseInterfaceCommand(InterfaceCommandWithListedOptionsABC[None]):
        @dataclass(kw_only=True)
        class Options(OptionsABC):
            LayoutItemInstance: LayoutItem.CoverableItem | LayoutItem.NonCoverableItem
            Position: int

    ToolSequence: str
    SupportedDeckLocations: list[DeckLocation.Base.DeckLocationABC]
    SupportedLabwares: list[Labware.Base.LabwareABC]
    Open: OpenCloseInterfaceCommand = field(init=False)
    Close: OpenCloseInterfaceCommand = field(init=False)

    @abstractmethod
    def _Open(self, Options: list[OpenCloseInterfaceCommand.Options]):
        ...

    @abstractmethod
    def _OpenTime(self, Options: list[OpenCloseInterfaceCommand.Options]) -> float:
        ...

    @abstractmethod
    def _Close(self, Options: list[OpenCloseInterfaceCommand.Options]):
        ...

    @abstractmethod
    def _CloseTime(self, Options: list[OpenCloseInterfaceCommand.Options]) -> float:
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
