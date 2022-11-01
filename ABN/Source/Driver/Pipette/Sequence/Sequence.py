from ....AbstractClasses import ObjectABC
from ....API.Tools.Container import Container


class Sequence(ObjectABC):
    def __init__(
        self,
        Well: int,
        DestinationContainerInstance: Container,
        SourceContainerInstance: Container,
        AspirateMixCycles: int,
        DispenseMixCycles: int,
        TransferVolume: float,
    ):
        self.Well: int = Well

        self.DestinationContainerInstance: Container = DestinationContainerInstance
        self.SourceContainerInstance: Container = SourceContainerInstance

        self.AspirateMixCycles: int = AspirateMixCycles
        self.DispenseMixCycles: int = DispenseMixCycles

        self.TransferVolume: float = TransferVolume

    def GetName(self) -> int:
        return self.Well

    def GetDestinationContainer(self) -> Container:
        return self.DestinationContainerInstance

    def GetSourceContainer(self) -> Container:
        return self.SourceContainerInstance

    def GetAspirateMixCycles(self) -> int:
        return self.AspirateMixCycles

    def GetDispenseMixCycles(self) -> int:
        return self.DispenseMixCycles

    def GetTransferVolume(self) -> float:
        return self.TransferVolume
