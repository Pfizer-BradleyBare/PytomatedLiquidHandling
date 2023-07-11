from dataclasses import dataclass, field
from threading import Lock
from typing import Generic, TypeVar

from ..Object.NonUniqueObjectABC import NonUniqueObjectABC

T = TypeVar("T", bound="NonUniqueObjectABC")


@dataclass
class NonUniqueObjectTrackerABC(Generic[T]):
    """This is a 'smart' tracker for classes the extend the non-unique object class.
    This class is generic such that it can track any class or set of classes."""

    Collection: list[T] = field(init=False, default_factory=list)
    ThreadLock: Lock = field(init=False, default=Lock())

    def LoadSingle(self, ObjectABCInstance: T) -> None:
        if ObjectABCInstance in self.Collection:
            raise Exception(
                type(ObjectABCInstance).__name__
                + " was added as a duplicate instance. This is illegal."
            )

        self.Collection.append(ObjectABCInstance)

    def UnloadSingle(self, ObjectABCInstance: T) -> None:
        if not ObjectABCInstance in self.Collection:
            raise Exception(type(ObjectABCInstance).__name__ + " does not exist.")
        self.Collection.remove(ObjectABCInstance)

    def LoadList(self, ObjectABCInstances: list[T]) -> None:
        for ObjectABCInstance in ObjectABCInstances:
            self.LoadSingle(ObjectABCInstance)

    def UnloadList(self, ObjectABCInstances: list[T]) -> None:
        for ObjectABCInstance in ObjectABCInstances:
            self.UnloadSingle(ObjectABCInstance)

    def IsTracked(self, ObjectABCInstance: T) -> bool:
        BoolTest = ObjectABCInstance in self.Collection

        return BoolTest

    def GetNumObjects(self) -> int:
        Length = len(self.Collection)

        return Length

    def GetObjectsAsList(self) -> list[T]:
        List = self.Collection

        return List

    def GetObjectsByName(self, UniqueIdentifier: str | int) -> list[T]:
        Objects = list()

        for Object in self.Collection:
            if Object.Identifier == UniqueIdentifier:
                Objects.append(Object)

        return Objects
