from .....Tools.AbstractClasses import UniqueObjectABC
from .ReservableLid import ReservableLid


class LidReservation(UniqueObjectABC):
    def __init__(self, UniqueIdentifier: str, ReservableLidInstance: ReservableLid):
        UniqueObjectABC.__init__(self, UniqueIdentifier)
        self.ReservableLidInstance: ReservableLid = ReservableLidInstance
