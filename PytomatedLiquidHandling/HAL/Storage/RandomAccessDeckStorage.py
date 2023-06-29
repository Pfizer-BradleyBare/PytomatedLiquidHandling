from dataclasses import dataclass

from ..LayoutItem.BaseLayoutItem import LayoutItemABC
from .BaseStorage import Reservation, Storage


@dataclass
class RandomAccessDeckStorage(Storage):
    def Reserve(self, LayoutItemInstance: LayoutItemABC) -> LayoutItemABC:
        if self.CheckReservationExists(LayoutItemInstance) == True:
            raise Exception(
                "Reservation with this UniqueIdentifier already found. Use a different ID."
            )

        SupportedLabwareInstances = [
            LayoutItemInstance.LabwareInstance
            for LayoutItemInstance in self.ReservableLayoutItemTrackerInstance.GetObjectsAsList()
        ]

        if not LayoutItemInstance.LabwareInstance in SupportedLabwareInstances:
            raise Exception("This labware is not supported by this storage object")

        AvailablePositions = [
            Position
            for Position in self.ReservableLayoutItemTrackerInstance.GetObjectsAsList()
            if Position.DeckLocationInstance
            not in [
                Reservation.LayoutItemInstance.DeckLocationInstance
                for Reservation in self.ReservationTrackerInstance.GetObjectsAsList()
            ]
        ]

        if len(AvailablePositions) == 0:
            raise Exception("No more storage positions available")

        LayoutItemInstance = AvailablePositions[0]

        self.ReservationTrackerInstance.LoadSingle(
            Reservation(LayoutItemInstance.UniqueIdentifier, LayoutItemInstance)
        )

        return LayoutItemInstance

    def PreTransportCheck(self, LayoutItemInstance: LayoutItemABC):
        if self.CheckReservationExists(LayoutItemInstance) == False:
            raise Exception("No lid storage reservation found. Please reserve first.")

    def Release(self, LayoutItemInstance: LayoutItemABC):
        if self.CheckReservationExists(LayoutItemInstance) == False:
            raise Exception("No lid storage reservation found. Please reserve first.")

        self.ReservationTrackerInstance.UnloadSingle(
            self.ReservationTrackerInstance.GetObjectByName(
                LayoutItemInstance.UniqueIdentifier
            )
        )
