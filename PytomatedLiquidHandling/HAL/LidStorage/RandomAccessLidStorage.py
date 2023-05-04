from PytomatedLiquidHandling.HAL.LayoutItem import Lid

from ..LayoutItem import Lid
from .BaseLidStorage import LidReservation, LidStorage


class RandomAccessLidStorage(LidStorage):
    def __init__(self, UniqueIdentifier: str):
        LidStorage.__init__(self, UniqueIdentifier)

    def Reserve(self, UniqueIdentifier: str) -> Lid:
        if self.__CheckReservationExists(UniqueIdentifier) == True:
            raise Exception(
                "Lid reservation with this UniqueIdentifier already found. Use a different ID."
            )

        AvailableLids = [
            Lid
            for Lid in self.GetObjectsAsList()
            if Lid not in self.LidReservationTrackerInstance.GetObjectsAsList()
        ]

        if len(AvailableLids) == 0:
            raise Exception("No more lid storage positions available")

        ReservableLidInstance = AvailableLids[0]
        self.LidReservationTrackerInstance.ManualLoad(
            LidReservation(UniqueIdentifier, ReservableLidInstance)
        )

        return ReservableLidInstance

    def PreTransportCheck(self, UniqueIdentifier: str):
        if self.__CheckReservationExists(UniqueIdentifier) == False:
            raise Exception("No lid storage reservation found. Please reserve first.")

    def Release(self, UniqueIdentifier: str):
        if self.__CheckReservationExists(UniqueIdentifier) == False:
            raise Exception("No lid storage reservation found. Please reserve first.")

        self.LidReservationTrackerInstance.ManualUnload(
            self.LidReservationTrackerInstance.GetObjectByName(UniqueIdentifier)
        )
