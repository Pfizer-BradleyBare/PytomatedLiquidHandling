from abc import abstractmethod
from ..Object.ObjectABC import ObjectABC

# This is an abstract loader class for loading configuration files


class TrackerABC:
    @abstractmethod
    def __init__(self):
        self.Collection: dict[str, ObjectABC] = dict()

    @abstractmethod
    def LoadManual(self, ObjectABCInstance: ObjectABC):
        raise NotImplementedError

    @abstractmethod
    def GetObjectsAsList(self) -> list[ObjectABC]:
        return self.Collection.items()

    @abstractmethod
    def GetObjectsAsDictionary(self) -> dict[str, ObjectABC]:
        return self.Collection

    @abstractmethod
    def GetObjectByName(self, Name: str) -> ObjectABC:
        return self.Collection[Name]
