from dataclasses import dataclass

from PytomatedLiquidHandling.HAL import LayoutItem

from .Base import StorageDeviceABC
from .Base.Reservation import Reservation


@dataclass
class RandomAccessDeckStorage(StorageDeviceABC):
    def Reserve(self, ReservationID: str, LayoutItem: LayoutItem.Base.LayoutItemABC):
        if ReservationID in self.Reservations:
            raise Exception("Reservation ID already exists")

        ReservedSites = [
            Site.LayoutItem.DeckLocation for Site in self.Reservations.values()
        ]

        ReservationLabware = LayoutItem.Labware

        FreeSites = [
            Site
            for Site in self.ReservableLayoutItems
            if Site.Labware == ReservationLabware
            and Site.DeckLocation not in ReservedSites
        ]
        # site must support the labware and must also not overlap with already reserved deck locations

        if len(FreeSites) == 0:
            raise Exception(
                "No sites available..."
            )  # Could we potentially move something? Thought...

        self.Reservations[ReservationID] = Reservation(FreeSites[0])

    def Release(self, ReservationID: str):
        if ReservationID not in self.Reservations:
            raise Exception("Reservation ID does not exist")

        Reservation = self.Reservations[ReservationID]

        if Reservation.IsStored == True:
            raise Exception(
                "You must remove the object from storage before you can release the reservation"
            )

        del self.Reservations[ReservationID]

    def PrepareStore(self, ReservationID: str):
        ...

    def Store(self, ReservationID: str) -> LayoutItem.Base.LayoutItemABC:
        if ReservationID not in self.Reservations:
            raise Exception("Reservation ID does not exist")

        Reservation = self.Reservations[ReservationID]

        if Reservation.IsStored == True:
            raise Exception("Object already stored")

        Reservation.IsStored = True

        return Reservation.LayoutItem

    def PrepareRetrieve(self, ReservationID: str):
        ...

    def Retrieve(self, ReservationID: str) -> LayoutItem.Base.LayoutItemABC:
        if ReservationID not in self.Reservations:
            raise Exception("Reservation ID does not exist")

        Reservation = self.Reservations[ReservationID]

        if Reservation.IsStored == False:
            raise Exception("Object not yet stored")

        Reservation.IsStored = False

        return Reservation.LayoutItem
