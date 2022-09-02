from abc import abstractmethod

# This is an abstract loader class for loading configuration files


class TrackerABC:
    @abstractmethod
    def __init__(self):
        self.Collection = dict()

    @abstractmethod
    def LoadManual(self, Object):
        raise NotImplementedError

    @abstractmethod
    def GetObjectsAsList(self):
        return self.Collection.items()

    @abstractmethod
    def GetObjectsAsDictionary(self):
        return self.Collection

    @abstractmethod
    def GetObjectByName(self, Name: str):
        return self.Collection[Name]
