from threading import Lock
from typing import Generic, TypeVar

from ..Object.NonUniqueObjectABC import NonUniqueObjectABC

T = TypeVar("T", bound="NonUniqueObjectABC")


class NonUniqueObjectTrackerABC(Generic[T]):
    """This is a 'smart' tracker for classes the extend the non-unique object class.
    This class is generic such that it can track any class or set of classes."""

    def __init__(self):
        self.Collection: list[T] = list()
        self.ThreadLock: Lock = Lock()

    def LoadSingle(self, ObjectABCInstance: T) -> None:
        self.Collection.append(ObjectABCInstance)

    def UnloadSingle(self, ObjectABCInstance: T) -> None:
        self.Collection.remove(ObjectABCInstance)

    def LoadList(self, ObjectABCInstances: list[T]) -> None:
        for ObjectABCInstance in ObjectABCInstances:
            self.LoadSingle(ObjectABCInstance)

    def UnloadList(self, ObjectABCInstances: list[T]) -> None:
        for ObjectABCInstance in ObjectABCInstances:
            self.UnloadSingle(ObjectABCInstance)

    def GetNumObjects(self) -> int:
        Length = len(self.Collection)

        return Length

    def GetObjectsAsList(self) -> list[T]:
        List = self.Collection

        return List

    def GetObjectsByName(self, UniqueIdentifier: str | int) -> list[T]:
        Objects = list()

        for Object in self.Collection:
            if Object.GetIdentifier() == UniqueIdentifier:
                Objects.append(Object)

        return Objects
