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
