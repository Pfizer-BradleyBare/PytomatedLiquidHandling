from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from PytomatedLiquidHandling.HAL import DeckLocation, TempControlDevice
from PytomatedLiquidHandling.Tools.BaseClasses import (
    UniqueObjectABC,
    UniqueObjectTrackerABC,
)

if TYPE_CHECKING:
    from ..Orchastrator import Orchastrator


_ReservableTypes = (
    TempControlDevice.BaseTempControlDevice.TempControlDevice
    | DeckLocation.Base.DeckLocationABC
)


@dataclass
class ResourceReservation:
    OrchastratorInstance: Orchastrator
    Reservations: UniqueObjectTrackerABC[_ResourceReservation] = field(
        init=False, default_factory=UniqueObjectTrackerABC
    )
    ReservedObjects: UniqueObjectTrackerABC[_ReservableTypes] = field(
        init=False, default_factory=UniqueObjectTrackerABC
    )

    @dataclass
    class _ResourceReservation(UniqueObjectABC):
        ReservedObject: _ReservableTypes
        Strict: bool

    def Acquire(
        self,
        UniqueIdentifier: str,
        ObjectInstance: _ReservableTypes,
        Strict: bool = False,
    ):
        Instance = self._ResourceReservation(UniqueIdentifier, ObjectInstance, Strict)

        self.Reservations.LoadSingle(Instance)

        self.ReservedObjects.LoadSingle(ObjectInstance)

    def GetReservation(self, UniqueIdentifier: str) -> _ResourceReservation:
        return self.Reservations.GetObjectByName(UniqueIdentifier)

    def Release(self, Reservation: _ResourceReservation):
        self.Reservations.UnloadSingle(Reservation)

        self.ReservedObjects.UnloadSingle(Reservation.ReservedObject)

    def IsObjectReserved(self, ObjectInstance: _ReservableTypes):
        return self.ReservedObjects.IsTracked(ObjectInstance.UniqueIdentifier)
