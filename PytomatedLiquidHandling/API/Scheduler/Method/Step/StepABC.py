from abc import abstractmethod
from dataclasses import dataclass

from PytomatedLiquidHandling.API.Tools import ResourceReservation
from PytomatedLiquidHandling.HAL import HAL
from PytomatedLiquidHandling.Tools.AbstractClasses import UniqueObjectABC


@dataclass
class StepABC(UniqueObjectABC):
    @abstractmethod
    def Execute(
        self,
        Simulate: bool,
        HALInstance: HAL,
        ResourceReservationTrackerInstance: ResourceReservation.ResourceReservationTracker,
    ):
        ...
