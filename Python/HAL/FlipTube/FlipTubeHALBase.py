from abc import abstractmethod, ABC


class FlipTubeHALBase(ABC):
    @abstractmethod
    def HALFlipTubeInitialize(self):
        pass

    @abstractmethod
    def HALFlipTubeOpen(self):
        pass

    @abstractmethod
    def HALFlipTubeClose(self):
        pass
