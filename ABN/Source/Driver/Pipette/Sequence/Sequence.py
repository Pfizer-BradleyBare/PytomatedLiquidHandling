from ....Tools.AbstractClasses import ObjectABC
from ....API.Tools.Container import ContainerOperator


class Sequence(ObjectABC):
    def __init__(
        self,
        Well: int,
        DestinationContainerOperatorInstance: ContainerOperator,
        SourceContainerOperatorInstance: ContainerOperator,
        AspirateMixCycles: int,
        DispenseMixCycles: int,
        TransferVolume: float,
    ):
        self.Well: int = Well

        self.DestinationContainerOperatorInstance: ContainerOperator = (
            DestinationContainerOperatorInstance
        )
        self.SourceContainerOperatorInstance: ContainerOperator = (
            SourceContainerOperatorInstance
        )

        self.AspirateMixCycles: int = AspirateMixCycles
        self.DispenseMixCycles: int = DispenseMixCycles

        self.TransferVolume: float = TransferVolume

    def GetName(self) -> int:
        return self.Well

    def GetDestinationContainerOperator(self) -> ContainerOperator:
        return self.DestinationContainerOperatorInstance

    def GetSourceContainerOperator(self) -> ContainerOperator:
        return self.SourceContainerOperatorInstance

    def GetAspirateMixCycles(self) -> int:
        return self.AspirateMixCycles

    def GetDispenseMixCycles(self) -> int:
        return self.DispenseMixCycles

    def GetTransferVolume(self) -> float:
        return self.TransferVolume
