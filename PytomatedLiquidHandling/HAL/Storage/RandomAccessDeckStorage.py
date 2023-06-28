from dataclasses import dataclass

from ..LayoutItem.BaseLayoutItem import LayoutItemABC
from .BaseStorage import Reservation, Storage


@dataclass
class RandomAccessDeckStorage(Storage):
    def Reserve(self, UniqueIdentifier: str) -> LayoutItemABC:
        if self.CheckReservationExists(UniqueIdentifier) == True:
            raise Exception(
                "Lid reservation with this UniqueIdentifier already found. Use a different ID."
            )

        AvailablePositions = [
            Position
            for Position in self.ReservableLidTrackerInstance.GetObjectsAsList()
            if Position
            not in [
                Reservation.LayoutItemInstance
                for Reservation in self.ReservationTrackerInstance.GetObjectsAsList()
            ]
        ]

        if len(AvailablePositions) == 0:
            raise Exception("No more storage positions available")

        LayoutItemInstance = AvailablePositions[0]

        self.ReservationTrackerInstance.LoadSingle(
            Reservation(UniqueIdentifier, LayoutItemInstance)
        )

        return LayoutItemInstance

    def PreTransportCheck(self, UniqueIdentifier: str):
        if self.CheckReservationExists(UniqueIdentifier) == False:
            raise Exception("No lid storage reservation found. Please reserve first.")

    def Release(self, UniqueIdentifier: str):
        if self.CheckReservationExists(UniqueIdentifier) == False:
            raise Exception("No lid storage reservation found. Please reserve first.")

        self.ReservationTrackerInstance.UnloadSingle(
            self.ReservationTrackerInstance.GetObjectByName(UniqueIdentifier)
        )
