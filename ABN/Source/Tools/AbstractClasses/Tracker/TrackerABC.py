from typing import Generic, TypeVar

from ..Object.ObjectABC import ObjectABC

T = TypeVar("T", bound="ObjectABC")


class TrackerABC(Generic[T]):
    def __init__(self):
        self.Collection: dict[str | int, T] = dict()

    def ManualLoad(self, ObjectABCInstance: T) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                type(ObjectABCInstance).__name__
                + " is already tracked. Name: "
                + str(Name)
            )

        self.Collection[Name] = ObjectABCInstance

    def ManualUnload(self, ObjectABCInstance: T) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is False:
            raise Exception(
                type(ObjectABCInstance).__name__
                + " is not yet tracked. Name: "
                + str(Name)
            )

        del self.Collection[Name]

    def IsTracked(self, ObjectABCInstance: T) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    def GetNumObjects(self) -> int:
        return len(self.Collection)

    def GetObjectsAsList(self) -> list[T]:
        return [self.Collection[Key] for Key in self.Collection]

    def GetObjectsAsDictionary(self) -> dict[str | int, T]:
        return self.Collection

    def GetObjectByName(self, Name: str | int) -> T:
        return self.Collection[Name]
