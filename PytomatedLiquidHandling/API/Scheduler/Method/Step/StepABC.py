from abc import abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, Self, Type

from PytomatedLiquidHandling.API.Tools import ResourceReservation
from PytomatedLiquidHandling.HAL import HAL
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC


@dataclass
class StepABC(UniqueObjectABC):
    AllStepClasses: ClassVar[list[Type[Self]]] = field(init=False, default_factory=list)
    PreExecuteComplete: bool = field(init=False, default=False)
    StepExecutionBlock: list[Type[Self]] = field(init=False, default_factory=list)

    def __init_subclass__(cls) -> None:
        StepABC.AllStepClasses.append(cls)

    def PreExecute(
        self,
        Simulate: bool,
        HALInstance: HAL,
        ResourceReservationTrackerInstance: ResourceReservation.ResourceReservationTracker,
    ):
        self.PreExecuteComplete = True

    @abstractmethod
    def Execute(
        self,
        Simulate: bool,
        HALInstance: HAL,
        ResourceReservationTrackerInstance: ResourceReservation.ResourceReservationTracker,
    ):
        ...
