from threading import Lock
from typing import Generic, TypeVar

from ..Object.ObjectABC import ObjectABC

T = TypeVar("T", bound="ObjectABC")


class TrackerABC(Generic[T]):
    def __init__(self):
        self.Collection: dict[str | int, T] = dict()
        self.ThreadLock: Lock = Lock()

    def ManualLoad(self, ObjectABCInstance: T) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(Name) is True:
            raise Exception(
                type(ObjectABCInstance).__name__
                + " is already tracked. Name: "
                + str(Name)
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: T) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(Name) is False:
            raise Exception(
                type(ObjectABCInstance).__name__
                + " is not yet tracked. Name: "
                + str(Name)
            )

        del self.Collection[Name]

    def IsTracked(self, Name: str | int) -> bool:

        BoolTest = Name in self.Collection

        return BoolTest

    def GetNumObjects(self) -> int:

        Length = len(self.Collection)

        return Length

    def GetObjectsAsList(self) -> list[T]:

        List = [self.Collection[Key] for Key in self.Collection]

        return List

    def GetObjectsAsDictionary(self) -> dict[str | int, T]:

        Dict = self.Collection

        return Dict

    def GetObjectByName(self, Name: str | int) -> T:

        Object = self.Collection[Name]

        return Object
