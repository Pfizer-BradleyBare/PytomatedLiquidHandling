from pydantic import dataclasses

from plh.hal import LayoutItem

from .Base import StorageDeviceABC
from .Base.Reservation import Reservation


@dataclasses.dataclass(kw_only=True)
class RandomAccessDeckStorage(StorageDeviceABC):
    def Reserve(self, ReservationID: str, LayoutItem: LayoutItem.Base.LayoutItemABC):
        if ReservationID in self._Reservations:
            raise Exception("Reservation ID already exists")

        ReservedSites = [
            Site.LayoutItem.DeckLocation for Site in self._Reservations.values()
        ]

        ReservationLabware = LayoutItem.Labware

        FreeSites = [
            Site
            for Site in self.LayoutItems
            if Site.Labware == ReservationLabware
            and Site.DeckLocation not in ReservedSites
        ]
        # site must support the labware and must also not overlap with already reserved deck locations

        if len(FreeSites) == 0:
            raise Exception(
                "No sites available...",
            )  # Could we potentially move something? Thought...

        self._Reservations[ReservationID] = Reservation(LayoutItem=FreeSites[0])

    def Release(self, ReservationID: str):
        if ReservationID not in self._Reservations:
            raise Exception("Reservation ID does not exist")

        Reservation = self._Reservations[ReservationID]

        if Reservation._IsStored == True:
            raise Exception(
                "You must remove the object from storage before you can release the reservation",
            )

        del self._Reservations[ReservationID]

    def PrepareStore(self, ReservationID: str):
        ...

    def Store(self, ReservationID: str) -> LayoutItem.Base.LayoutItemABC:
        if ReservationID not in self._Reservations:
            raise Exception("Reservation ID does not exist")

        Reservation = self._Reservations[ReservationID]

        if Reservation._IsStored == True:
            raise Exception("Object already stored")

        Reservation._IsStored = True

        return Reservation.LayoutItem

    def PrepareRetrieve(self, ReservationID: str):
        ...

    def Retrieve(self, ReservationID: str) -> LayoutItem.Base.LayoutItemABC:
        if ReservationID not in self._Reservations:
            raise Exception("Reservation ID does not exist")

        Reservation = self._Reservations[ReservationID]

        if Reservation._IsStored == False:
            raise Exception("Object not yet stored")

        Reservation._IsStored = False

        return Reservation.LayoutItem
