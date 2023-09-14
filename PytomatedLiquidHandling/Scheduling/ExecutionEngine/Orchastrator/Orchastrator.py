from __future__ import annotations

from dataclasses import dataclass, field

from PytomatedLiquidHandling import HAL

from .ContainerLoader import ContainerLoader
from .RecurringNotification import RecurringNotification
from .ResourceReservation import ResourceReservation
from .Timer import Timer


@dataclass
class Orchastrator:
    HALInstance: HAL.HAL

    Timer: Timer = field(init=False)
    RecurringNotification: RecurringNotification = field(init=False)
    ResourceReservation: ResourceReservation = field(init=False)
    ContainerLoader: ContainerLoader = field(init=False)

    def __post_init__(self):
        self.Timer = Timer(self)
        self.RecurringNotification = RecurringNotification(self)
        self.ResourceReservation = ResourceReservation(self)
        self.ContainerLoader = ContainerLoader(self)
