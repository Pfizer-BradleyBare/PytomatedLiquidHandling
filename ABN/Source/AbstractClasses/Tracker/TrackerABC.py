from abc import abstractmethod
from ..Object.ObjectABC import ObjectABC


class TrackerABC:
    @abstractmethod
    def __init__(self):
        self.Collection: dict[str, ObjectABC] = dict()

    @abstractmethod
    def ManualLoad(self, ObjectABCInstance: ObjectABC):
        raise NotImplementedError

    @abstractmethod
    def ManualUnload(self, ObjectABCInstance: ObjectABC):
        raise NotImplementedError

    @abstractmethod
    def IsTracked(self, ObjectABCInstance: ObjectABC):
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
