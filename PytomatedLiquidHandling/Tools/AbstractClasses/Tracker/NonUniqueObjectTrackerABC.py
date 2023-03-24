from threading import Lock
from typing import Generic, TypeVar

from ..Object.NonUniqueObjectABC import NonUniqueObjectABC

T = TypeVar("T", bound="NonUniqueObjectABC")


class NonUniqueObjectTrackerABC(Generic[T]):
    def __init__(self):
        self.Collection: list[T] = list()
        self.ThreadLock: Lock = Lock()

    def ManualLoad(self, ObjectABCInstance: T) -> None:

        self.Collection.append(ObjectABCInstance)

    def ManualUnload(self, ObjectABCInstance: T) -> None:

        self.Collection.remove(ObjectABCInstance)

    def GetNumObjects(self) -> int:

        Length = len(self.Collection)

        return Length

    def GetObjectsAsList(self) -> list[T]:

        List = self.Collection

        return List
