from threading import Lock
from typing import Generic, TypeVar

from ..Object.UniqueObjectABC import UniqueObjectABC

T = TypeVar("T", bound="UniqueObjectABC")


class UniqueObjectTrackerABC(Generic[T]):
    """This is a 'smart' tracker for classes the extend the unique object class.
    This class is generic such that it can track any class or set of classes."""

    def __init__(self):
        self.Collection: dict[str | int, T] = dict()
        self.ThreadLock: Lock = Lock()

    def ManualLoad(self, ObjectABCInstance: T) -> None:
        Name = ObjectABCInstance.GetUniqueIdentifier()

        if self.IsTracked(Name) is True:
            raise Exception(
                type(ObjectABCInstance).__name__
                + " is already tracked. UniqueIdentifier: "
                + str(Name)
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: T) -> None:
        Name = ObjectABCInstance.GetUniqueIdentifier()

        if self.IsTracked(Name) is False:
            raise Exception(
                type(ObjectABCInstance).__name__
                + " is not yet tracked. UniqueIdentifier: "
                + str(Name)
            )

        del self.Collection[Name]

    def IsTracked(self, UniqueIdentifier: str | int) -> bool:
        BoolTest = UniqueIdentifier in self.Collection

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

    def GetObjectByName(self, UniqueIdentifier: str | int) -> T:
        Object = self.Collection[Name]

        return Object
