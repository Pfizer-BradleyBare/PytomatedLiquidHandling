from abc import abstractmethod
from ..Object.ObjectABC import ObjectABC

# NOTE: This is an abstract base class but for all intents and purposes the methods can be directly copied and used. However,
# do not forget to change the type information!


class TrackerABC:
    @abstractmethod
    def __init__(self):
        self.Collection: dict[str, ObjectABC] = dict()

    @abstractmethod
    def ManualLoad(self, ObjectABCInstance: ObjectABC) -> None:

        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is already tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    @abstractmethod
    def ManualUnload(self, ObjectABCInstance: ObjectABC) -> None:
        Name = ObjectABCInstance.GetName()

        if self.IsTracked(ObjectABCInstance) is True:
            raise Exception(
                str(type(ObjectABCInstance).__name__)
                + " is not yet tracked. Name: "
                + Name
            )

        self.Collection[Name] = ObjectABCInstance

    @abstractmethod
    def IsTracked(self, ObjectABCInstance: ObjectABC) -> bool:
        return ObjectABCInstance.GetName() in self.Collection

    @abstractmethod
    def GetObjectsAsList(self) -> list[ObjectABC]:
        return list(self.Collection.items())

    @abstractmethod
    def GetObjectsAsDictionary(self) -> dict[str, ObjectABC]:
        return self.Collection

    @abstractmethod
    def GetObjectByName(self, Name: str) -> ObjectABC:
        return self.Collection[Name]
