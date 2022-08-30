from abc import ABC, abstractmethod

# This is an abstract loader class for loading configuration files


class TrackerABC(ABC):
    @abstractmethod
    def __init__(self):
        self.Collection = dict()

    @abstractmethod
    def LoadManual(self, Object):
        raise NotImplementedError

    @abstractmethod
    def GetLoadedObjectsAsList(self):
        return self.Collection.items()

    @abstractmethod
    def GetLoadedObjectsAsDictionary(self):
        return self.Collection
