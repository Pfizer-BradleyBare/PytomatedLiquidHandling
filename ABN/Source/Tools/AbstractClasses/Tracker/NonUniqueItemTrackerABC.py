from threading import Lock
from typing import Generic, TypeVar

from ..Object.ObjectABC import ObjectABC

T = TypeVar("T", bound="ObjectABC")


class NonUniqueItemTrackerABC(Generic[T]):
    def __init__(self):
        self.Collection: list[T] = list()
        self.ThreadLock: Lock = Lock()

    def ManualLoad(self, ObjectABCInstance: T) -> None:

        self.Collection.append(ObjectABCInstance)

    def ManualUnload(self, ObjectABCInstance: T) -> None:

        self.Collection.remove(ObjectABCInstance)

    def IsTracked(self, Name: str | int) -> bool:

        Names = [Item.GetName() for Item in self.Collection]

        BoolTest = Name in Names

        return BoolTest

    def GetNumObjects(self) -> int:

        Length = len(self.Collection)

        return Length

    def GetObjectsAsList(self) -> list[T]:

        List = self.Collection

        return List

    def GetObjectsAsDictionary(self) -> dict[str | int, T]:

        Names = [Item.GetName() for Item in self.Collection]

        if len(self.Collection) != len(set(Names)):
            raise Exception(
                "Items are not all unique so a Dictionary cannot be created."
            )

        Dict = {Item.GetName(): Item for Item in self.Collection}

        return Dict

    def GetObjectByName(self, Name: str | int) -> T:

        Names = [Item.GetName() for Item in self.Collection]

        try:
            Index = Names.index(Name)
        except:
            raise Exception("Name not found.")

        Object = self.Collection[Index]

        return Object
