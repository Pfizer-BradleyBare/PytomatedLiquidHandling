from PytomatedLiquidHandling.HAL.LayoutItem import Lid

from ..LayoutItem import Lid
from .BaseLidStorage import LidReservation, LidStorage
from dataclasses import dataclass


@dataclass
class RandomAccessLidStorage(LidStorage):
    def Reserve(self, UniqueIdentifier: str) -> Lid:
        if self.CheckReservationExists(UniqueIdentifier) == True:
            raise Exception(
                "Lid reservation with this UniqueIdentifier already found. Use a different ID."
            )

        AvailableLids = [
            Lid
            for Lid in self.ReservableLidTrackerInstance.GetObjectsAsList()
            if Lid
            not in [
                Reservation.LidInstance
                for Reservation in self.LidReservationTrackerInstance.GetObjectsAsList()
            ]
        ]

        if len(AvailableLids) == 0:
            raise Exception("No more lid storage positions available")

        LidInstance = AvailableLids[0]
        if not isinstance(LidInstance, Lid):
            raise Exception("This should never happen")

        self.LidReservationTrackerInstance.LoadSingle(
            LidReservation(UniqueIdentifier, LidInstance)
        )

        return LidInstance

    def PreTransportCheck(self, UniqueIdentifier: str):
        if self.CheckReservationExists(UniqueIdentifier) == False:
            raise Exception("No lid storage reservation found. Please reserve first.")

    def Release(self, UniqueIdentifier: str):
        if self.CheckReservationExists(UniqueIdentifier) == False:
            raise Exception("No lid storage reservation found. Please reserve first.")

        self.LidReservationTrackerInstance.UnloadSingle(
            self.LidReservationTrackerInstance.GetObjectByName(UniqueIdentifier)
        )
