from PytomatedLiquidHandling.API.Tools import Container
from PytomatedLiquidHandling.HAL import HeatCoolShakeDevices


class Reservation:
    Temperature: float
    RPM: int
    Container: Container.Container


Reservations: dict[str, Reservation] = dict()


def Reserve(Container: Container.Container, Temperature: float, RPM: int):
    ...


def UpdateReservation(Container: Container.Container, Temperature: float, RPM: int):
    ...


def Release(Container: Container.Container):
    ...


def Start(Container: Container.Container):
    ...


def Stop(Container: Container.Container):
    ...
