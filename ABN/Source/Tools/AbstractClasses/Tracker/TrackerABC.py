from threading import Lock
from typing import Generic, TypeVar

from ..Object.ObjectABC import ObjectABC

T = TypeVar("T", bound="ObjectABC")


class TrackerABC(Generic[T]):
    def __init__(self):
        self.Collection: dict[str | int, T] = dict()
        self.ThreadLock: Lock = Lock()

    def ManualLoad(self, ObjectABCInstance: T) -> None:

        self.ThreadLock.acquire()

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(Name) is True:
            raise Exception(
                type(ObjectABCInstance).__name__
                + " is already tracked. Name: "
                + str(Name)
            )

        self.Collection[Name] = ObjectABCInstance

        self.ThreadLock.release()

    def ManualUnload(self, ObjectABCInstance: T) -> None:

        self.ThreadLock.acquire()

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(Name) is False:
            raise Exception(
                type(ObjectABCInstance).__name__
                + " is not yet tracked. Name: "
                + str(Name)
            )

        del self.Collection[Name]

        self.ThreadLock.release()

    def IsTracked(self, Name: str | int) -> bool:
        self.ThreadLock.acquire()

        BoolTest = Name in self.Collection

        self.ThreadLock.release()

        return BoolTest

    def GetNumObjects(self) -> int:
        self.ThreadLock.acquire()

        Length = len(self.Collection)

        self.ThreadLock.release()

        return Length

    def GetObjectsAsList(self) -> list[T]:
        self.ThreadLock.acquire()

        List = [self.Collection[Key] for Key in self.Collection]

        self.ThreadLock.release()

        return List

    def GetObjectsAsDictionary(self) -> dict[str | int, T]:
        self.ThreadLock.acquire()

        Dict = self.Collection

        self.ThreadLock.release()

        return Dict

    def GetObjectByName(self, Name: str | int) -> T:
        self.ThreadLock.acquire()

        Object = self.Collection[Name]

        self.ThreadLock.release()

        return Object
